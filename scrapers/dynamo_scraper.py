from datetime import datetime
import requests
from lxml import html
import re

from scrapers.restaurant_scraper import RestaurantScraper, Dish


class DynamoScraper(RestaurantScraper):

    def __init__(self):
        super().__init__()
        self.name = 'Dynamo'
        self.icon = ':radio:'
        self.color = '#70031b'
        self.link = 'https://www.dynamorestaurace.cz/clanky/poledni-menu/'
        self.scrape()

    def scrape(self):
        response = requests.get(self.link)

        tree = html.fromstring(response.content)

        today = datetime.today()
        date_str = tree.xpath('(//table//td//p | //table//td//p//strong)/text()')
        if not date_str:
            return
        date_str = date_str[0]
        try:
            menu_date = datetime.strptime(re.split('\s', date_str.strip())[-1], '%d.%m.%Y')
        except ValueError:
            return

        if today.date() != menu_date.date():
            return

        rows = tree.xpath('//table//tr')
        for row in rows:
            columns = [c.strip() for c in row.xpath('./td//text()') if c.strip()]
            if not columns or len(columns) < 2:
                continue
            name = re.sub(r'\s+', ' ', re.sub(r'\s?_\s?', ' ', columns[0]))
            price = columns[1] + ' Kč'

            self.dish_array.append(
                Dish(name, price)
            )
