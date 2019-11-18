from datetime import datetime
import requests
from lxml import html

from scrapers.restaurant_scraper import RestaurantScraper, Dish


class SrdcovkaScraper(RestaurantScraper):

    def __init__(self):
        super().__init__()
        self.name = 'Srdcovka Spálená'
        self.icon = ':hearts:'
        self.color = '#bd1934'
        self.link = 'https://www.gambrinus.cz/srdcovka/spalena'
        self.scrape()

    def scrape(self):
        response = requests.get(self.link)

        tree = html.fromstring(response.content)

        today = datetime.today()
        date_str = tree.xpath('//div[@class="denne-menu"]//span[@class="h3"]//text()')
        if not date_str:
            return
        date_str = date_str[0]
        menu_date = datetime.strptime(date_str.split(' ')[-1], '%d.%m.%Y')

        if today.date() != menu_date.date():
            return

        li_elements = tree.xpath('//ul[@class="food-menu"]//li')

        for elements in li_elements:
            text_elements = elements.xpath('.//text()')

            name = text_elements[0].strip()
            price = text_elements[-1].replace('-', '').strip()

            self.dish_array.append(
                Dish(name, price)
            )
