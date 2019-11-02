from scrapers.zomato_scraper import ZomatoScraper


class SerialBurgersScraper(ZomatoScraper):
    def __init__(self):
        super().__init__()
        self.res_id = 16506026

        self.name = 'Serial Burgers'
        self.icon = ':knife:'
        self.color = '#282a36'
        self.scrape()
