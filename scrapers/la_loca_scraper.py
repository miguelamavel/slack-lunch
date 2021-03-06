from datetime import datetime
import requests
from lxml import html

from scrapers.restaurant_scraper import RestaurantScraper, Dish
from utils import cz_months_map, cz_weekdays, cz_weekday_map


class LaLocaScraper(RestaurantScraper):

    def __init__(self):
        super().__init__()
        self.name = 'La Loca'
        self.icon = ':mushroom:'
        self.color = '#c43025'
        self.link = 'https://togethertastesbetter.cz/obedove-menu'
        self.scrape()

    @staticmethod
    def translate_date(date_str):
        elements = date_str.split('.')
        day_str = elements[0].strip()
        month_str = elements[1].strip()

        eng_date = day_str + ' ' + cz_months_map[month_str].capitalize()

        return datetime.strptime(eng_date, '%d %B')

    def scrape(self):
        response = requests.get(self.link)

        tree = html.fromstring(response.content)

        today = datetime.today()
        date_str = tree.xpath('//h3/text()')[0].split(' - ')
        start_date = self.translate_date(date_str[0].lower())
        end_date = self.translate_date(date_str[1].lower())

        if not (start_date.day <= today.day <= end_date.day and start_date.month <= today.month <= end_date.month):
            return

        p_elements = tree.xpath('//div[@class="sqs-block-content"]//p')

        dishes = {
            'Pondělí': [], 'Úterý': [], 'Středa': [], 'Čtvrtek': [], 'Pátek': []
        }
        current_day = None

        for p in p_elements:
            inner_text = ''.join(p.xpath('.//text()')).strip()
            if current_day == 'Pátek' and p.xpath('./@data-rte-preserve-empty') and 'true' in p.xpath('./@data-rte-preserve-empty')[0]:
                break

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
