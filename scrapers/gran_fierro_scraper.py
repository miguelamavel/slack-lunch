from datetime import datetime
import requests
from lxml import html
import re

from scrapers.restaurant_scraper import RestaurantScraper, Dish


class GranFierroScraper(RestaurantScraper):

    def __init__(self):
        super().__init__()
        self.name = 'Gran Fierro'
        self.icon = ':cow2:'
        self.color = '#51ddfc'
        self.link = 'https://granfierro.cz/'
        self.scrape()

    def scrape(self):
        response = requests.get(self.link)

        tree = html.fromstring(response.content)

        today = datetime.today()
        date_str = tree.xpath('//span[contains(string(), "POLEDNÍ MENU")]/text()')
        if not date_str:
            return
        date_str = date_str[0]
        menu_date = datetime.strptime(date_str.split(' ')[-1], '%d.%m.%Y')

        if today.date() != menu_date.date():
            return

        div = tree.xpath('//div[@class="flexbox"]//div[@class="news-header"]')[0]
        dishes = [''.join(elem.xpath('.//text()')) for elem in div.xpath('(.//p | .//figcaption)')]

        for dish in dishes:
            if 'polední menu' in dish.lower():
                continue
            text_elements = re.split(r'[\s+]?[–\-]\s+', dish)
            if len(text_elements) > 2:
                text_elements = [' - '.join(text_elements[:-1]), text_elements[-1]]

            if len(text_elements) != 2:
                continue

            name = re.sub(r'\s+', ' ', text_elements[0]).strip()
            price = text_elements[1].strip()

            self.dish_array.append(
                Dish(name, price)
            )
