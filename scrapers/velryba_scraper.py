import requests
from lxml import html

from scrapers.restaurant_scraper import RestaurantScraper, Dish


class VelrybaScraper(RestaurantScraper):

    def __init__(self):
        super().__init__()
        self.name = 'Velryba'
        self.icon = ':whale:'
        self.color = '#397ea3'

    def scrape(self):
        response = requests.get('https://www.kavarnavelryba.cz/polednimenu/')

        tree = html.fromstring(response.content)

        dish_elements = tree.xpath('//li[@class="menu-list__item"]')

        for elem in dish_elements:
            name = ' '.join(elem.xpath('.//*[not(@class="menu-list__item-price")]/text()'))
            name = name.replace('  ', ' ')
            price = elem.xpath('.//span[@class="menu-list__item-price"]/text()')[0]

            if not name or not price:
                continue

            self.dish_array.append(
                Dish(name, price)
            )
