import re
from datetime import datetime
import requests
from lxml import html

from scrapers.restaurant_scraper import RestaurantScraper, Dish
from utils import cz_weekday_map


class EstrellaScraper(RestaurantScraper):

    def __init__(self):
        super().__init__()
        self.name = 'Estrella'
        self.icon = ':star:'
        self.color = '#f0dd0a'
        self.link = 'http://estrellarestaurant.cz/index.php/denni-menu/'
        self.scrape()

        self.tree = None

    @staticmethod
    def separate_dish_price(string):
        return tuple([s.strip() for s in re.split('_+', string)])

    def get_dish(self, title):
        special = self.tree.xpath('//p[contains(string(), "%s")]/following-sibling::p[1]//text()' % title)
        special = ''.join(special)

        name, price = self.separate_dish_price(special)
        return name, price

    def scrape(self):
        response = requests.get(self.link)

        self.tree = html.fromstring(response.content)

        today = datetime.today()
        title_string = today.strftime('%-d.%-m')
        padded_title_string = today.strftime('%d.%m')

        today_element = self.tree.xpath('//div[@class="dine-menu-wrapper" and '
                                        '(contains(string(), "%s") or contains(string(), "%s"))]'
                                        % (title_string, padded_title_string))

        if not today_element:
            return

        today_element = today_element[0]
        names = today_element.xpath('.//h3//text()')
        prices = today_element.xpath('.//span[@class="menu-item-price"]//text()')

        for name, price in zip(names, prices):
            if name.lower() == 'combo':
                continue
            self.dish_array.append(
                Dish(name.replace(' - ', ', ').strip(), price.strip())
            )


        wrappers = self.tree.xpath('//div[@class="dine-menu-wrapper"]')
        h2_wrappers = [w.xpath('.//h2//text()')[0].lower() for w in wrappers]

        if 'specialita týdne' in h2_wrappers:
            special_idx = h2_wrappers.index('specialita týdne')
        elif 'speciality týdne' in h2_wrappers:
            special_idx = h2_wrappers.index('speciality týdne')
        else:
            return

        special_items = wrappers[special_idx].xpath('.//div[@class="dine-menu-item"]')

        if len(special_items) != 3:
            return

        name = special_items[0].xpath('.//h3//text()')[0].replace(' - ', ', ').strip()
        price = special_items[0].xpath('.//span[@class="menu-item-price"]//text()')[0].replace('CZK', 'Kč')

        self.dish_array.append(
            Dish('*Specialita:* ' + name, price)
        )

        name = special_items[1].xpath('.//div[@class="menu-item-desc"]//text()')[0].replace(' - ', ', ').strip()
        price = special_items[1].xpath('.//span[@class="menu-item-price"]//text()')[0].replace('CZK', 'Kč')

        self.dish_array.append(
            Dish('*Salát/Lehké jídlo:* ' + name, price)
        )

        name = special_items[2].xpath('.//div[@class="menu-item-desc"]//text()')[0].replace(' - ', ', ').strip()
        price = special_items[2].xpath('.//span[@class="menu-item-price"]//text()')[0].replace('CZK', 'Kč')

        self.dish_array.append(
            Dish('*Desert:* ' + name, price)
        )
