import scrapy
import re
import json


class PerfumeSpider(scrapy.Spider):
    name = "perfume"
    allowed_domains = ["cologneculture.com"]
    start_urls = ["https://cologneculture.com/collections/all?page=1"]
    base_url = "https://cologneculture.com"

    def parse(self, response):
        products = response.css("div.grid-view-item.product-card")

        for link in products.css("a::attr(href)").getall():
            perfume_link = self.base_url + link
            yield scrapy.Request(perfume_link, callback=self.parse_perfume)

        next_page_partial_url = response.css(
            "a.btn.btn--tertiary.btn--narrow::attr(href)"
        ).getall()[-1]
        next_page_url = self.base_url + next_page_partial_url
        yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_perfume(self, response):

        # name = response.css("h1.product-single__title::text").get()
        # price = response.css("span.money::text").get()
        # size_selection = response.css("div.product-form__controls-group")
        # sizes = size_selection.css("option::text").getall()

        # Get Prices
        js_data = re.findall("var meta =(.+?);\n", response.body.decode("utf-8"), re.S)
        ls = json.loads(js_data[0])

        product_variants = ls["product"]["variants"]

        name = []
        price = []

        for i in range(len(product_variants)):
            name.append(product_variants[i]["name"])
            price.append(product_variants[i]["price"] / 100.0)

        yield {"name": name, "price": price}
