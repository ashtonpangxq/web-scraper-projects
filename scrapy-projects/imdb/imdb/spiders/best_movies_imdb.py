import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesImdbSpider(CrawlSpider):
    name = "best_movies_imdb"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]

    rules = (
        Rule(
            LinkExtractor(restrict_xpaths="//td[@class='titleColumn']"),
            callback="parse_item",
            follow=True,
        ),
    )

    def parse_item(self, response):
        yield {
            "title": response.xpath("//h1/text()").get(),
            "year": response.xpath(
                "//h1/following-sibling::node()/ul/li[1]/a/text()"
            ).get(),
            "duration": "".join(
                response.xpath(
                    "//h1/following-sibling::node()/ul/li[3]/text()"
                ).getall()
            ),
            "genre": response.xpath(
                "//div[contains(@class, 'ipc-chip-list--baseAlt')]/div[@class='ipc-chip-list__scroller']/a/span/text()"
            ).getall(),
            "rating": response.xpath(
                "//div[@data-testid='hero-rating-bar__aggregate-rating__score'][1]/span[1]/text()"
            ).get(),
            "movie_url": response.url,
        }
