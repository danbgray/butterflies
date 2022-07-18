import scrapy
import string
import re
from scrapy import Request


def remove_html_tags(text):
    tag_re = re.compile(r'<[^>]+>|\n|\r|:')
    return tag_re.sub('', text).rstrip()


class ButterflySpider(scrapy.Spider):
    """ The beginning of a spider to obtain catalog of information from butterfliesofamerica.com """

    name = "ButterflyGlossary"
    base_url = 'https://butterfliesofamerica.com/'
    start_urls = ["{}{}".format(base_url, "US-Can-Cat.htm"),]

    def parse(self, response):
        """ Parse the one-page contents of the glossary page """

        # Assemble the list of acronyms
        acrynym_xpath = '/html/body/div[2]/div[2]/div//p'
        museums_list = response.xpath(acrynym_xpath).extract()
        for museum in museums_list:
            museum_abbreviation = museum.split("</b>")
            yield {"museum": remove_html_tags(museum_abbreviation[1]),
                   "acronym": remove_html_tags(museum_abbreviation[0])}
