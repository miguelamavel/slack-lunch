from scrapers.chilli_point_scraper import ChilliPointScraper
from scrapers.estrella_scraper import EstrellaScraper
from scrapers.jina_krajina_scraper import JinaKrajinaScraper
from scrapers.karluv_sklep_scraper import KarluvSklepScraper
from scrapers.kathmandu_scraper import KathmanduScraper
from scrapers.la_loca_scraper import LaLocaScraper
from scrapers.lemon_leaf_scraper import LemonLeafScraper
from scrapers.serial_burgers_scraper import SerialBurgersScraper
from scrapers.srdcovka_scraper import SrdcovkaScraper
from scrapers.the_nest_scraper import TheNestScraper
from scrapers.velryba_scraper import VelrybaScraper
from slack_client import SlackClient
import os

if __name__ == '__main__':
    scrapers = [
        KarluvSklepScraper(),
        SrdcovkaScraper(),
        VelrybaScraper(),
        SerialBurgersScraper(),
        JinaKrajinaScraper(),
        ChilliPointScraper(),
        KathmanduScraper(),
        TheNestScraper(),
        LemonLeafScraper(),
        LaLocaScraper(),
        EstrellaScraper(),
    ]

    client = SlackClient(os.environ['SLACK_ACCESS_TOKEN'], '#test_channel')

    for scraper in scrapers:
        client.add_menu(scraper.name,
                        scraper.dish_array,
                        restaurant_icon=scraper.icon,
                        color=scraper.color,
                        link=scraper.link)

    client.write_menu()