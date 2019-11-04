from scrapers.zomato_scraper import ZomatoScraper


class SerialBurgersScraper(ZomatoScraper):
    def __init__(self):
        super().__init__()
        self.res_id = 18257533

        self.name = 'Serial Burgers'
        self.icon = ':knife:'
        self.color = '#282a36'
        self.link = 'https://www.zomato.com/praha/serial-burgers-nov%C3%A9-m%C4%9Bsto-praha-1/daily-menu'
        self.scrape()
