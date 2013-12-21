# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class URLItem(Item):
    title = Field()
    urlAddress = Field()
    document_text = Field()
