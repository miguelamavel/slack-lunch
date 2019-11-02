from datetime import datetime

import requests
from lxml import html
import re

from scrapers.restaurant_scraper import RestaurantScraper, Dish

cz_months_map = {
    'leden': 'january',
    'únor': 'february',
    'březen': 'march',
    'duben': 'april',
    'květen': 'may',
    'červen': 'june',
    'červenec': 'july',
    'srpen': 'august',
    'září': 'september',
    'říjen': 'october',
    'listopad': 'november',
    'prosinec': 'december',
}

cz_weekdays = ['Pondělí', 'Úterý', 'Středa', 'Čtvrtek', 'Pátek']
cz_weekday_map = {
    0: 'Pondělí',
    1: 'Úterý',
    2: 'Středa',
    3: 'Čtvrtek',
    4: 'Pátek',
}


class LaLocaScraper(RestaurantScraper):

    def __init__(self):
        super().__init__()
        self.name = 'La Loca'
        self.icon = ':mushroom:'
        self.color = '#c43025'
        self.scrape()

    @staticmethod
    def translate_date(date_str):
        elements = date_str.split('. ')
        day_str = elements[0]
        month_str = elements[1]

        eng_date = day_str + ' ' + cz_months_map[month_str].capitalize()

        return datetime.strptime(eng_date, '%d %B')

    def scrape(self):
        response = requests.get('https://togethertastesbetter.cz/obedove-menu')

        tree = html.fromstring(response.content)

        today = datetime.today()
        date_str = tree.xpath('//h3/text()')[0].split(' - ')
        start_date = self.translate_date(date_str[0].lower())
        end_date = self.translate_date(date_str[1].lower())

        if not (start_date.day < today.day < end_date.day and start_date.month < today.month < end_date.month):
            return

        p_elements = tree.xpath('//div[@class="sqs-block-content"]//p')

        dishes = {
            'Pondělí': [], 'Úterý': [], 'Středa': [], 'Čtvrtek': [], 'Pátek': []
        }
        current_day = None

        for p in p_elements:
            inner_text = ''.join(p.xpath('.//text()')).strip()
            if not inner_text:
                continue
            if inner_text in cz_weekdays:
                current_day = inner_text
            else:
                dishes[current_day].append(inner_text)

        today_weekday = today.weekday()
        if today_weekday in cz_weekday_map and cz_weekday_map[today_weekday] in dishes:
            today_dishes = dishes[cz_weekday_map[today_weekday]]
            for dish in today_dishes:
                separated = dish.rsplit('.', -1)
                name = separated[0]
                price = separated[1] + ' Kč'
                self.dish_array.append(
                    Dish(name, price)
                )
