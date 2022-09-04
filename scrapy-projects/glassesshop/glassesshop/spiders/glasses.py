import scrapy


class GlassesSpider(scrapy.Spider):
    name = "glasses"
    allowed_domains = ["www.glassesshop.com"]

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.glassesshop.com/bestsellers",
            callback=self.parse,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
            },
        )

    def parse(self, response):
        products = response.xpath(
            "//div[@id='product-lists']/div[@class='col-12 pb-5 mb-lg-3 col-lg-4 product-list-row text-center product-list-item']"
        )

        for product in products:
            product_url = product.xpath(
                ".//div[@class='product-img-outer']/a[1]/@href"
            ).get()
            # product_name = product.xpath(".//div[@class='product-img-outer']/a[1]/@href").get()
            product_name = product.xpath(
                ".//div[@class='product-img-outer']/a[1]/img[@class='lazy d-block w-100 product-img-default']/@alt"
            ).get()
            image_url = product.xpath(
                ".//div[@class='product-img-outer']/a[1]/img[1]/@data-src"
            ).get()
            price = product.xpath(
                ".//div[@class='p-title-block']//div[@class='p-price']/div[1]/span/text()"
            ).get()

            yield {
                "product_url": product_url,
                "product_name": product_name,
                "image_url": image_url,
                "price": price,
            }

        next_page = response.xpath(
            "//div[@class='row mt-5 mb-5 d-none d-lg-block']//ul//li[last()]/a/@href"
        ).get()

        if next_page:
            yield response.follow(url=next_page, callback=self.parse)
