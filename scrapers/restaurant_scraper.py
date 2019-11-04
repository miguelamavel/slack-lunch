from typing import List

from dish import Dish


class RestaurantScraper:
    name: str
    dish_array: List[Dish]
    icon: str
    color: str
    link: str

    def __init__(self):
        self.dish_array = []
        self.icon = None
        self.color = None

    def scrape(self):
        raise NotImplementedError