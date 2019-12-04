import requests
from lxml import html

from dish import Dish
from scrapers.restaurant_scraper import RestaurantScraper


class TheNestScraper(RestaurantScraper):

    def __init__(self):
        super().__init__()
        self.name = 'The Nest'
        self.icon = ':hatching_chick:'
        self.color = '#07a37f'
        self.link = 'https://thenestprague.cz/poledni-nabidka-2/'
        self.scrape()

    def scrape(self):
        response = requests.get(self.link)

        tree = html.fromstring(response.content)

        image_url = tree.xpath('//figure/img/@src')
        if not image_url:
            return
        self.link = image_url[0]

        self.dish_array.append(
            Dish('Click the restaurant link to check the weekly menu', '')
        )
