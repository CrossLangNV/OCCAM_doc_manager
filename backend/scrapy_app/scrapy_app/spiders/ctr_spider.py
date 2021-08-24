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

        print(f"Started '{self.name}' scraper for company number: ", company_number)
        print("URL: ", url)
        yield scrapy.Request(url, self.parse_ctr_publications)

    def parse_ctr_publications(self, response):
        start = time.time()

        identification_number = str(self.company_number).strip()
        print("Started scrapy 'parse_ctr_publications' request for company number: ", identification_number)

        selector = Selector(text=response.text)
        # aunp-content
        items = selector.xpath('//div[@class="aunp-content"]')
        print("items: ", items)

        try:
            company = CtrCompany.objects.get(identification_number=identification_number)
        except CtrCompany.DoesNotExist:
            company = CtrCompany.objects.create(identification_number=identification_number)

        # print("response.txt: ", response.text)

        for item in items:
            name = selector.xpath('//div[@class="vr-hlavicka"]/text()').extract()
            print(f"name: {name}")

            value = item.xpath('td[2]/text()').extract()
            links = item.xpath('td[1]//a/@href').extract()
            links_text = item.xpath('td[1]//a/text()').extract()

            # Find external links and linked entities
            if links:
                pass

            if not value:
                # If value of text() is empty, it will probably be in another tag
                value = item.xpath('td[2]').extract()

            if value:
                value = remove_html_and_tabs(value[0])
            if name:
                name = remove_html_and_tabs(name)

            if name:
                print(f"{name}: {value}")

                if name == LEGAL_STATUS:
                    company.state = value

                elif name == LEGAL_STATUS:
                    company.legal_status = value

            company.save()

        exec_time = time.time() - start
        print(f"Scraping completed in {exec_time} seconds")


def remove_html_and_tabs(text):
    return ' '.join(BeautifulSoup(text, "lxml").text.split())
