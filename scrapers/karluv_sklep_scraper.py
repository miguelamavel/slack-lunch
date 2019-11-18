import re
import requests
from lxml import html

from scrapers.restaurant_scraper import RestaurantScraper, Dish


class KarluvSklepScraper(RestaurantScraper):

    def __init__(self):
        super().__init__()
        self.name = 'Karluv Sklep'
        self.icon = ':flag-cz:'
        self.color = '#161bb5'
        self.link = 'http://www.karluvsklep.cz/Poledni_Mednu'
        self.scrape()

    def scrape(self):
        response = requests.get(self.link)

        tree = html.fromstring(response.content)

        p_elements = tree.xpath('//div[@class="field-items"]//p')

        prev_text = None
        for elements in p_elements:
            text_elements = elements.xpath('.//text()')
            text = ' '.join(text_elements).replace('  ', ' ').strip()

            if text_elements and re.match(r'\d+,-', text_elements[-1]):
                name = ' '.join(text_elements[:-1]).replace('  ', ' ').strip()
                if prev_text and prev_text not in ['Hotová jídla', 'Polévky']:
                    name = prev_text + ' ' + name

                price = text_elements[-1][:-2] + ' Kč'
                self.dish_array.append(
                    Dish(name, price)
                )

            prev_text = text
