from datetime import datetime
import requests
from lxml import html

from scrapers.restaurant_scraper import RestaurantScraper, Dish


class ChilliPointScraper(RestaurantScraper):

    def __init__(self):
        super().__init__()
        self.name = 'Chilli Point'
        self.icon = ':hot_pepper:'
        self.color = '#b8220b'
        self.link = 'https://www.chillipoint.cz/'
        self.scrape()

    def scrape(self):
        response = requests.get(self.link)

        tree = html.fromstring(response.content)

        today = datetime.today()

        menu_table = tree.xpath('//div[@class="row sketches-menu"]//h3[contains(text(), "%s")]'
                                '/following-sibling::ul' % today.strftime('%d. %m. %Y'))
        if not menu_table:
            return

        for dish_element in menu_table[0].xpath('.//li'):
            name = dish_element.xpath('./text()')[0].strip()
            price = dish_element.xpath('./span/text()')[0].strip()

            self.dish_array.append(
                Dish(name, price)
            )
