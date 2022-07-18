import scrapy
import string
from scrapy import Request

class ButterflySpider(scrapy.Spider):
    """ The beginning of a spider to obtain catalog of information from butterfliesofamerica.com """

    name = "ButterflyMeta"
    start_urls = ['https://butterfliesofamerica.com/list.htm']
    base_url = 'https://butterfliesofamerica.com/'

    def parse(self, response):

        # The table name on the list page that has all of the links we want to fetch
        # just called "table1"

        xp = '//*[@id="table1"]//td[1]//a/@href'
        urls = response.xpath(xp).extract()
        return ( Request("{}{}".format(self.base_url,url), callback=self.parse_detail_page)
                 for url in urls)

    def parse_detail_page(self, response):
        """ For a detail page """
        
        images = response.xpath("//img/@src").extract()
        yield {"images": images}
