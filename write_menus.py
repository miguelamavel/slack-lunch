from scrapers.velryba_scraper import VelrybaScraper
from slack_client import SlackClient
import os

if __name__ == '__main__':
    client = SlackClient(os.environ['SLACK_ACCESS_TOKEN'], '#test_channel')

    scrapers = [
        VelrybaScraper()
    ]

    for scraper in scrapers:
        client.add_menu(scraper.name,
                        scraper.dish_array,
                        restaurant_icon=scraper.icon,
                        color=scraper.color)

    client.write_menu()