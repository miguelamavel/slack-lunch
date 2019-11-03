import re
from datetime import datetime
import requests
from lxml import html

from scrapers.restaurant_scraper import RestaurantScraper, Dish
from utils import cz_weekdays, cz_weekday_map

protected_texts = ['Polévka', 'Hlavní chod', 'Hlavní chody', 'bez polévky']

class KathmanduScraper(RestaurantScraper):

    def __init__(self):
        super().__init__()
        self.name = 'Kathmandu'
        self.icon = ':flag-np:'
        self.color = '#1224b0'
        self.scrape()

    def scrape(self):
        response = requests.get('https://www.restauracekathmandu.cz/denni-menu')

        tree = html.fromstring(response.content)

        today = datetime.today()

        elements = tree.xpath('(//p | //ol/li)//text()')

        dishes = {
            'Pondělí': [], 'Úterý': [], 'Středa': [], 'Čtvrtek': [], 'Pátek': []
        }
        current_day = None

        for inner_text in elements:
            inner_text = inner_text.strip()
            if not inner_text:
                continue
            first_part = inner_text.split('/')[0]
            if first_part.capitalize() in cz_weekdays:
                current_day = first_part.capitalize()
            elif current_day and first_part not in protected_texts:
                dishes[current_day].append(inner_text)

        today_weekday = today.weekday()
        if today_weekday in cz_weekday_map and cz_weekday_map[today_weekday] in dishes:
            today_dishes = dishes[cz_weekday_map[today_weekday]]
            for dish in today_dishes:
                if len(self.dish_array) < 2:
                    self.dish_array.append(
                        Dish(dish, '+ 10 Kč')
                    )
                else:
                    separated_prices = re.split('\s\s+', dish)
                    if len(separated_prices) > 1:
                        self.dish_array.append(
                            Dish(separated_prices[0], separated_prices[1].split(',')[0] + ' Kč')
                        )
