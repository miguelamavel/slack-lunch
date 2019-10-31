from dish import Dish
from slack_client import SlackClient
import os

if __name__ == '__main__':
    client = SlackClient(os.environ['SLACK_ACCESS_TOKEN'], '#test_channel')
    client.add_menu('Maison Amavel',
                    [Dish('Meat', '500 Kc'), Dish('Fish', '550 Kc')],
                    restaurant_icon=':whale:')
    client.write_menu()