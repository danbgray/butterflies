import scrapy
import bs4 as BeautifulSoup
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

        # Assemble the list of acronyms for museums
        acrynym_xpath = '/html/body/div[2]/div[2]/div//p'
        museums_list = response.xpath(acrynym_xpath).extract()
        for museum in museums_list:
            museum_abbreviation = museum.split("</b>")
            yield {"museum": remove_html_tags(museum_abbreviation[1]),
                   "acronym": remove_html_tags(museum_abbreviation[0])}

        # Get all of the main headings.
        p = response.xpath("/html/body/div[2]/p[*]").extract()

        # Start with class 'p1' headings.  Associate following content with that.
        # Grab the main headings

        _b = '<p class="p1">'
        _e = '</p>'

        headings = []
        for ps in p:
            if '<p class="p1">' in ps:
                headings += [ps.replace(_b,'').replace(_e,'')]
        yield {"headings": headings}
