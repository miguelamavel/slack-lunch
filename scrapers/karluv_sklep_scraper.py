import re
from datetime import datetime

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
        checked_date = False

        for elements in p_elements:
            text_elements = elements.xpath('.//text()')
            text = ' '.join(text_elements).replace('  ', ' ').strip()

            if not text:
                continue

            if not checked_date and text:
                today = datetime.today()
                nums = re.findall('\d+', text)
                checked_date = True
                if len(nums) != 2 or int(nums[0]) != today.day or int(nums[1]) != today.year:
                    return
                continue

            if text in ['Polední menu', 'Hotová jídla', 'Polévky']:
                continue

            if text_elements and re.match(r'\d+,-?', text_elements[-1]) and not re.match(r'\d,\d', text_elements[-1]):
                name = ' '.join(text_elements[:-1]).replace('  ', ' ').strip()
                if prev_text:
                    name = prev_text + ' ' + name
                prev_text = None

                price = text_elements[-1].replace(',', '').replace('-', '').strip() + ' Kč'
                self.dish_array.append(
                    Dish(name, price)
                )
                continue

            if 'font-size: medium;' not in elements.xpath('.//span/@style'):
                prev_text = prev_text + '\n' + text if prev_text else text
            else:
                prev_text = prev_text + ' ' + text if prev_text else text
