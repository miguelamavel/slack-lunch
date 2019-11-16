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
        self.link = 'http://www.estrellarestaurant.cz/denni-menu'
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
        title_string = cz_weekday_map[today.weekday()].upper() + ' ' + today.strftime('%-d.%-m.')

        dishes_path = '//p[contains(string(), "%s")]' \
                      '/following-sibling::p[position() >= 1 and position() <= 2]//text()' % title_string
        menu = self.tree.xpath(dishes_path)
        menu_price = ''.join(self.tree.xpath('//em[contains(string(), "hlavní")]//text()'))

        if not menu:
            return

        self.dish_array.append(
            Dish(menu[0], '+ 30 / 50  Kč (malá / velká)')
        )
        self.dish_array.append(
            Dish(menu[1], self.separate_dish_price(menu_price)[1])
        )

        name, price = self.get_dish('SPECIALITA')
        self.dish_array.append(
            Dish('*Specialita:* ' + name, price)
        )

        name, price = self.get_dish('SALÁT / LEHKÉ JÍDLO')
        self.dish_array.append(
            Dish('*Salát/Lehké jídlo:* ' + name, price)
        )

        name, price = self.get_dish('DEZERT')
        self.dish_array.append(
            Dish('*Dezert:* ' + name, price)
        )
