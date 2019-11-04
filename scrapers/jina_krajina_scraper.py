from scrapers.zomato_scraper import ZomatoScraper


class JinaKrajinaScraper(ZomatoScraper):
    def __init__(self):
        super().__init__()
        self.res_id = 16506026

        self.name = 'Jiná Krajina'
        self.icon = ':earth_asia:'
        self.color = '#509617'
        self.scrape()
