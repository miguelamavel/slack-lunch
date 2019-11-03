from scrapers.kathmandu_scraper import KathmanduScraper
from scrapers.la_loca_scraper import LaLocaScraper
from scrapers.serial_burgers_scraper import SerialBurgersScraper
from scrapers.velryba_scraper import VelrybaScraper
from slack_client import SlackClient
import os

if __name__ == '__main__':
    client = SlackClient(os.environ['SLACK_ACCESS_TOKEN'], '#test_channel')

    scrapers = [
        KathmanduScraper(),
        LaLocaScraper(),
        VelrybaScraper(),
        SerialBurgersScraper(),
    ]

    for scraper in scrapers:
        client.add_menu(scraper.name,
                        scraper.dish_array,
                        restaurant_icon=scraper.icon,
                        color=scraper.color)

    client.write_menu()