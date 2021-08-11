import scrapy
from bs4 import BeautifulSoup
from scrapy import Selector

from kbo.models import Company

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
        company_number = str(self.company_number).strip()
        print("Started scrapy 'parse_kbo_publications' request for company number: ", company_number)

        selector = Selector(text=response.text)
        items = selector.xpath('//*[@id="table"]/table//tr')

        try:
            company = Company.objects.get(company_number=company_number)
            print("Ok, company does exist.......", company)
        except Company.DoesNotExist:
            print("Nope, it does not exist...... creating.....")
            company = Company.objects.create(company_number=company_number)
            print("Created........", company)

        print("company: ", company)

        for item in items[1:]:
            name = item.xpath('td[1]/text()').extract_first()
            value = item.xpath('td[2]/text()').extract()

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
                    print("Updated state. And it worked.")

                elif name == LEGAL_STATUS:
                    company.legal_status = value
                    print("Updated legal_status")

                elif name == START_DATE:
                    company.start_date = value
                    print("Updated start_date. And it worked.")

                elif name == NAME:
                    company.name = value
                    print("Updated name")

                elif name == ADDRESS:
                    value = item.xpath('td[2]').extract()
                    value_stripped = remove_html_and_tabs(value[0])
                    company.address = value_stripped
                    print("Updated address")

                elif name == PHONE_NUMBER:
                    company.phone_number = value
                    print("Updated phone_number")

                elif name == FAX_NUMBER:
                    company.fax_number = value
                    print("Updated fax_number")

                elif name == EMAIL:
                    company.email = value
                    print("Updated email")

                elif name == WEBSITE:
                    company.website = value
                    print("Updated website")

                elif str(name) == ENTITY_TYPE:
                    company.entity_type = value
                    print("Updated entity_type")

                elif name == LEGAL_FORM:
                    company.legal_form = value
                    print("Updated legal_form")

                elif name == CAPITAL:
                    company.capital = value
                    print("Updated capital")

                elif name == ANNUAL_MEETING:
                    company.annual_meeting = value
                    print("Updated annual_meeting")

                elif name == FISCAL_YEAR_END_DATE:
                    company.fiscal_year_end_date = value
                    print("Updated fiscal_year_end_date")

                elif name == START_DATE_EXCEPTIONAL_FINANCIAL_YEAR:
                    company.start_date_exceptional_financial_year = value
                    print("Updated start_date_exceptional_financial_year")

                elif name == END_DATE_EXCEPTIONAL_FINANCIAL_YEAR:
                    company.end_date_exceptional_financial_year = value
                    print("Updated end_date_exceptional_financial_year")

                elif name.startswith("BTW"):
                    # TODO
                    pass

            company.save()

        test_result = Company.objects.filter(company_number=self.company_number)
        print("test_result: ", test_result)


def remove_html_and_tabs(text):
    return ' '.join(BeautifulSoup(text, "lxml").text.split())
