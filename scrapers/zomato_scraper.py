import os
import requests

from scrapers.restaurant_scraper import RestaurantScraper, Dish


class ZomatoScraper(RestaurantScraper):

    def __init__(self):
        super().__init__()
        self.api_key = os.environ['ZOMATO_API_KEY']
        self.url = 'https://developers.zomato.com/api/v2.1/dailymenu?res_id=%d'
        self.res_id = None
        self.header = {
            'user_key': self.api_key
        }

    def scrape(self):
        url = self.url % self.res_id
        response = requests.get(url, headers=self.header)

        response_js = response.json()

        if 'daily_menus' not in response_js or not response_js['daily_menus']:
            return

        dish_list = response_js['daily_menus'][0]['daily_menu']['dishes']
        ids = [dish['dish']['dish_id'] for dish in dish_list]

        prev_dish = ''
        for i, dish in enumerate(dish_list):
            if dish['dish']['dish_id'] in ids[i + 1:]:
                continue

            name = dish['dish']['name'].replace('  ', ' ').strip()
            price = dish['dish']['price'].strip()

            if not name or not price:
                if name:
                    prev_dish = name
                continue

            if prev_dish:
                name = (prev_dish + ' ' + name).replace('  ', ' ').strip()
                prev_dish = ''

            self.dish_array.append(
                Dish(name, price)
            )
