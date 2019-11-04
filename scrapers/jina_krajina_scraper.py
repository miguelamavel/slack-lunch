from scrapers.zomato_scraper import ZomatoScraper


class JinaKrajinaScraper(ZomatoScraper):
    def __init__(self):
        super().__init__()
        self.res_id = 16506026

        self.name = 'Jiná Krajina'
        self.icon = ':earth_asia:'
        self.color = '#509617'
        self.link = 'https://www.zomato.com/praha/jin%C3%A1-krajina-nov%C3%A9-m%C4%9Bsto-praha-1/daily-menu'
        self.scrape()
