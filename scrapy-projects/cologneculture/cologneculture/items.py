# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags


def remove_currency(value):
    return value.replace("SGD", "").strip()


class PerfumeItem(scrapy.item):
    # define the fields for your item here like:
    name = scrapy.Field(
        input_processor=MapCompose(remove_tags), output_processor=TakeFirst()
    )
    price = scrapy.Field(
        input_processor=MapCompose(remove_tags, remove_currency),
        output_processor=TakeFirst(),
    )
    sizes = scrapy.Field(
        input_processor=MapCompose(remove_tags), output_processor=TakeFirst()
    )
