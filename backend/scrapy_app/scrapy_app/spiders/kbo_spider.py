import time

import scrapy
from bs4 import BeautifulSoup
from scrapy import Selector

from kbo.models import Company, BtwNacebelActivity, RszNacebelActivity, ExternalLink, LinkedEntity, Director

STATE = "Status:"
LEGAL_STATUS = "Rechtstoestand:"
START_DATE = "Begindatum:"
NAME = "Naam:"
ADDRESS = "Adres van de zetel:"
PHONE_NUMBER = "Telefoonnummer:"
FAX_NUMBER = "Faxnummer:"
EMAIL = "E-mail:"
WEBSITE = "Webadres:"
ENTITY_TYPE = "Type entiteit:"
LEGAL_FORM = "Rechtsvorm:"
CAPITAL = "Kapitaal"
ANNUAL_MEETING = "Jaarvergadering"
FISCAL_YEAR_END_DATE = "Einddatum boekjaar"
START_DATE_EXCEPTIONAL_FINANCIAL_YEAR = "Begindatum uitzonderlijk boekjaar"
END_DATE_EXCEPTIONAL_FINANCIAL_YEAR = "Einddatum uitzonderlijk boekjaar"

EXTERNAL_LINKS = ["http://www.ejustice.just.fgov.be", "http://cri.nbb.be", "https://www.socialsecurity.be"]
DIRECTOR_PREFIXES = ["Bestuurder", "Vaste vertegenwoordiger", "Gedelegeerd bestuurder"]

BASE_URL = 'https://kbopub.economie.fgov.be/kbopub/zoeknummerform.html?nummer='


class KboSpider(scrapy.Spider):
    name = 'KBO'

    def start_requests(self):
        url = BASE_URL
        company_number = getattr(self, 'company_number', None)
        if company_number is not None:
            url = url + company_number

        print(f"Started '{self.name}' scraper for company number: ", company_number)
        print("KBO Public Search URL: ", url)
        yield scrapy.Request(url, self.parse_kbo_publications)

    def parse_kbo_publications(self, response):
        start = time.time()

        company_number = str(self.company_number).strip()
        print("Started scrapy 'parse_kbo_publications' request for company number: ", company_number)

        selector = Selector(text=response.text)
        items = selector.xpath('//*[@id="table"]/table//tr')

        try:
            company = Company.objects.get(company_number=company_number)
        except Company.DoesNotExist:
            company = Company.objects.create(company_number=company_number)



        for item in items[1:]:
            name = item.xpath('td[1]/text()').extract_first()
            value = item.xpath('td[2]/text()').extract()
            links = item.xpath('td[1]//a/@href').extract()
            links_text = item.xpath('td[1]//a/text()').extract()

            # Find external links and linked entities
            if links:
                for i in range(len(links)):
                    if any(map(links[i].__contains__, EXTERNAL_LINKS)):
                        url = links[i]
                        name = links_text[i]
                        ExternalLink.objects.update_or_create(name=name, url=url, company=company)
                    else:
                        url = "https://kbopub.economie.fgov.be/kbopub/" + links[i]
                        name = links_text[i]
                        LinkedEntity.objects.update_or_create(name=name, url=url, company=company)

            if not value:
                # If value of text() is empty, it will probably be in another tag
                value = item.xpath('td[2]').extract()

            if value:
                value = remove_html_and_tabs(value[0])
            if name:
                name = remove_html_and_tabs(name)

            if name:
                print(f"{name}: {value}")

                if name == STATE:
                    company.state = value

                elif name == LEGAL_STATUS:
                    company.legal_status = value

                elif name == START_DATE:
                    company.start_date = value

                elif name == NAME:
                    company.name = value

                elif name == ADDRESS:
                    value = item.xpath('td[2]').extract()
                    value_stripped = remove_html_and_tabs(value[0])
                    company.address = value_stripped

                elif name == PHONE_NUMBER:
                    company.phone_number = value

                elif name == FAX_NUMBER:
                    company.fax_number = value

                elif name == EMAIL:
                    company.email = value

                elif name == WEBSITE:
                    company.website = value

                elif str(name) == ENTITY_TYPE:
                    company.entity_type = value

                elif name == LEGAL_FORM:
                    company.legal_form = value

                elif name == CAPITAL:
                    company.capital = value

                elif name == ANNUAL_MEETING:
                    company.annual_meeting = value

                elif name == FISCAL_YEAR_END_DATE:
                    company.fiscal_year_end_date = value

                elif name == START_DATE_EXCEPTIONAL_FINANCIAL_YEAR:
                    company.start_date_exceptional_financial_year = value

                elif name == END_DATE_EXCEPTIONAL_FINANCIAL_YEAR:
                    company.end_date_exceptional_financial_year = value

                elif name.startswith("BTW"):
                    BtwNacebelActivity.objects.update_or_create(name=name, company=company)

                elif name.startswith("RSZ"):
                    RszNacebelActivity.objects.update_or_create(name=name, company=company)

                elif name.startswith(tuple(DIRECTOR_PREFIXES)):
                    Director.objects.update_or_create(name=value, role=name, company=company)

            company.save()

        exec_time = time.time() - start
        print(f"Scraping completed in {exec_time} seconds")


def remove_html_and_tabs(text):
    return ' '.join(BeautifulSoup(text, "lxml").text.split())
