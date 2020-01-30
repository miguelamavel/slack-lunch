import re
from datetime import datetime
import requests
from lxml import html

from scrapers.restaurant_scraper import RestaurantScraper, Dish
from utils import cz_weekdays, cz_weekday_map, is_int

protected_texts = ['Polévka', 'Hlavní chod', 'Hlavní chody', 'bez polévky']

class KathmanduScraper(RestaurantScraper):

    def __init__(self):
        super().__init__()
        self.name = 'Kathmandu'
        self.icon = ':flag-np:'
        self.color = '#1224b0'
        self.link = 'https://www.restauracekathmandu.cz/denni-menu'
        self.scrape()

    def scrape(self):
        response = requests.get(self.link)

        tree = html.fromstring(response.content)

        today = datetime.today()

        elements = tree.xpath('(//p | //ol/li)//text()')

        dishes = {
            'Pondělí': [], 'Úterý': [], 'Středa': [], 'Čtvrtek': [], 'Pátek': []
        }
        current_day = None

        for inner_text in elements:
            inner_text = inner_text.strip()
            inner_text = inner_text.replace('Polévka/Soup:', '').strip()
            if not inner_text:
                continue
            first_part = inner_text.split('/')[0]
            if first_part.capitalize() in cz_weekdays:
                current_day = first_part.capitalize()
            elif current_day and first_part not in protected_texts:
                dishes[current_day].append(re.sub(r'^\d.\s', '', inner_text))

        today_weekday = today.weekday()
        if today_weekday in cz_weekday_map and cz_weekday_map[today_weekday] in dishes:
            today_dishes = dishes[cz_weekday_map[today_weekday]]
            for dish in today_dishes:
                detected_dish = re.findall(r'(.*)\s+(\d+),\s?-\s+(\d+),\s?-', dish)
                if len(self.dish_array) < 2:
                    self.dish_array.append(
                        Dish(dish, '+ 10 Kč')
                    )
                elif detected_dish:
                    separated = detected_dish[0]
                    dish_name = re.sub(r'\s+', ' ', separated[0]).strip()
                    price = separated[1]
                    if is_int(price):
                        self.dish_array.append(
                            Dish(dish_name, price + ' Kč')
                        )
