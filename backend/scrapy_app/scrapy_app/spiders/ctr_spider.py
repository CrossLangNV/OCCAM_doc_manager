import time

import scrapy
from bs4 import BeautifulSoup
from scrapy import Selector

from ctr.models import CtrCompany

DATE_OF_CREATION_AND_ENTRY = "Datum vzniku a zápisu:"
FILE_REFERENCE = "Spisová značka:"
BUSINESS_NAME = "Obchodní firma:"
LOCATION = "Sídlo:"
IDENTIFICATION_NUMBER = "Identifikační číslo:"
LEGAL_STATUS = "Právní forma:"
OBJECT_OF_BUSINESS = "Předmět podnikání:"

STATUTORY_BODY = "Statutární orgán:"
MANAGER = "Jednatel:"

NUMBER_OF_MEMBERS = "Počet členů:"
REPRESENTATION = "Způsob jednání:"

SHAREHOLDERS = "Společníci"
SHAREHOLDER = "Společník:"
SHARE = "Podíl:"
LIEN = "Zástavní právo:"

SHARE_CAPITAL = "Základní kapitál:"
OTHER_FACTS = "Ostatní skutečnosti:"

LEGAL_DOCUMENTS_URL = 'https://or.justice.cz/ias/ui/vypis-sl-firma?subjektId='
COMPANY_INFO_BASE_URL = 'https://or.justice.cz/ias/ui/rejstrik-firma.vysledky?subjektId='
COMPANY_INFO_BASE_PARAMS = '&typ=UPLNY'

EXAMPLE_COMPANY_SKODA = "423841"


class CtrSpider(scrapy.Spider):
    name = 'CTR'

    def start_requests(self):
        url = COMPANY_INFO_BASE_URL
        company_number = getattr(self, 'company_number', None)
        if company_number is not None:
            url = url + company_number + COMPANY_INFO_BASE_PARAMS

        print(f"Started '{self.name}' scraper for company number: {company_number}")
        print(f"URL: {url}")
        yield scrapy.Request(url, self.parse_ctr_publications)

    def parse_ctr_publications(self, response):
        start = time.time()

        identification_number = str(self.company_number).strip()
        print(f"Started scrapy 'parse_ctr_publications' request for company number: {identification_number}")

        selector = Selector(text=response.text)
        # aunp-content
        items = selector.xpath('//div[@class="aunp-content"]')
        # print("items: ", items)

        try:
            company = CtrCompany.objects.get(identification_number=identification_number)
        except CtrCompany.DoesNotExist:
            company = CtrCompany.objects.create(identification_number=identification_number)

        # This works as well, but almost impossible to map this

        # for item in items:
        #     vr_child_type = item.xpath('div[@class="vr-child"]//div[@class="vr-hlavicka"]//span[@class="nounderline"]/text()').extract()
        #     print("TYPE: ", vr_child_type)
        #
        #     vr_child_value = item.xpath('div[@class="vr-child"]//div[@class="div-cell"]//span/text()').extract()
        #     print("VALUE: ", vr_child_value)


        results = []
        soup = BeautifulSoup(response.text, "html.parser")
        link_count = 0
        for tag in soup.find_all("div", class_="vr-hlavicka"):
            title = ""
            # If we found a <hr> tag, we search for the first <a> tag
            # but if another <hr> has been found instead, then we skip this one because it does not have any files.
            for sib in tag.next_siblings:
                if sib.name == "div":
                    col_type = sib.find("div", class_="vr-hlavicka").get_text()
                    print("col_type: ", col_type)

                    # Skip first here because the first one is the type

                    values = []
                    for value in sib.find_all("div", class_="div-cell")[1:]:

                        values.append(remove_html_and_tabs(value.get_text()))
                    print("Values: ", values)


            print("\n")


        exec_time = time.time() - start
        print(f"Scraping completed in {exec_time} seconds")


def remove_html_and_tabs(text):
    return ' '.join(BeautifulSoup(text, "lxml").text.split())
