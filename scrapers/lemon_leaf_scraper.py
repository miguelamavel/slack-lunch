from datetime import datetime
import requests
from lxml import html

from scrapers.restaurant_scraper import RestaurantScraper, Dish
from utils import cz_weekday_map


class LemonLeafScraper(RestaurantScraper):

    def __init__(self):
        super().__init__()
        self.name = 'Lemon Leaf'
        self.icon = ':lemon:'
        self.color = '#90c234'
        self.scrape()

    def scrape(self):
        response = requests.get('https://www.lemon.cz/lunch-menu/')

        tree = html.fromstring(response.content)

        today = datetime.today()
        today_token = today.strftime('%-d. %-m. ') + cz_weekday_map[today.weekday()]
        h2_array = [h.strip() for h in tree.xpath('//h2/text()')]
        dates = [elem for sublist in [d.strip().split(' & ') for d in h2_array]
                 for elem in sublist]

        if today_token not in dates:
            return

        elements = tree.xpath('(//div[@class="lunch-food-item price-right"] | //h2)//text()')
        dishes = [e.strip() for e in elements if e.strip()]

        i = 0
        while today_token not in dishes[i]:
            i = i + 1
        i = i + 1

        lunches = tree.xpath('//article//table[@class="timetable"]//td[@class="day"]//text()')
        prices = tree.xpath('//article//table[@class="timetable"]//td[not(@class="day")]//text()')
        lunch_prices = dict(zip([l.capitalize() for l in lunches], prices))

        while i < len(dishes) and dishes[i] not in h2_array:
            if dishes[i] in ['1. chod', '2. chod', '3. chod', 'Polévka', 'Lunch 1', 'Lunch 2', 'Lunch 3']:
                price = '? Kč'
                if dishes[i] == 'Polévka':
                    price = lunch_prices['Lunch polévka'].strip()
                elif dishes[i] in lunch_prices:
                    price = lunch_prices[dishes[i]].strip()
                self.dish_array.append(
                    Dish(dishes[i + 1].capitalize(), price)
                )
            i = i + 1
