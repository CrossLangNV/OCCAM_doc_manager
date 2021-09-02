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
        #     vr_child_value = item.xpath('div[@class="vr-child"]//div[@class="div-cell"]//span/text()').extract()

        soup = BeautifulSoup(response.text, "html.parser")

        # Initialize all data, because it could be empty
        date_of_creation_and_registration = ""
        file_reference = ""
        business_name = ""
        location = ""
        identification_number = ""
        legal_status = ""
        object_of_business = ""
        statutory_body = ""
        manager = ""
        number_of_members = ""
        representation = ""
        shareholders = ""
        shareholder = ""
        share = ""
        lien = ""
        share_capital = ""
        other_facts = ""

        for tag in soup.find_all("div", class_="vr-hlavicka"):
            # If we found a <hr> tag, we search for the first <a> tag
            # but if another <hr> has been found instead, then we skip this one because it does not have any files.
            for sib in tag.next_siblings:
                if sib.name == "div":
                    col_type = sib.find("div", class_="vr-hlavicka").get_text()
                    # print("col_type: ", col_type)

                    # Skip first here because the first one is the type
                    values = []
                    for value in sib.find_all("div", class_="div-cell")[1:]:
                        if not value.get_text().startswith("zapsáno"):
                            values.append(remove_html_and_tabs(value.get_text()))

                    values_str = "\n".join(values)
                    # print("values_str: ", values_str)

                    if DATE_OF_CREATION_AND_ENTRY in col_type:
                        date_of_creation_and_registration = values_str

                    elif FILE_REFERENCE in col_type:
                        file_reference = values_str

                    elif BUSINESS_NAME in col_type:
                        business_name = values_str

                    elif LOCATION in col_type:
                        location = values_str

                    elif IDENTIFICATION_NUMBER in col_type:
                        identification_number = values_str

                    elif LEGAL_STATUS in col_type:
                        legal_status = values_str

                    elif OBJECT_OF_BUSINESS in col_type:
                        object_of_business = values_str

                    elif STATUTORY_BODY in col_type:
                        statutory_body = values_str

                    elif MANAGER in col_type:
                        manager = values_str

                    elif NUMBER_OF_MEMBERS in col_type:
                        number_of_members = values_str

                    elif REPRESENTATION in col_type:
                        representation = values_str

                    elif SHAREHOLDERS in col_type:
                        shareholders = values_str

                    elif SHAREHOLDER  in col_type:
                        shareholder = values_str

                    elif SHARE in col_type:
                        share = values_str

                    elif LIEN in col_type:
                        lien = values_str

                    elif SHARE_CAPITAL in col_type:
                        share_capital = values_str

                    elif OTHER_FACTS in col_type:
                        other_facts = values_str

        print("date_of_creation_and_registration: ", date_of_creation_and_registration)
        print("file_reference: ", file_reference)
        print("business_name: ", business_name)
        print("location: ", location)
        print("identification_number: ", identification_number)
        print("legal_status: ", legal_status)
        print("object_of_business: ", object_of_business)
        print("statutory_body: ", statutory_body)
        print("manager: ", manager)
        print("number_of_members: ", number_of_members)
        print("representation: ", representation)
        print("shareholders: ", shareholders)
        print("shareholder: ", shareholder)
        print("share: ", share)
        print("lien: ", lien)
        print("share_capital: ", share_capital)
        print("other_facts: ", other_facts)

        company.date_of_creation_and_registration = date_of_creation_and_registration
        company.file_reference = file_reference
        company.business_name = business_name
        company.location = location
        company.legal_status = legal_status
        company.object_of_business = object_of_business
        company.statutory_body = statutory_body
        company.manager = manager
        company.number_of_members = number_of_members
        company.representation = representation
        company.shareholders = shareholders
        company.shareholder = shareholder
        company.share = share
        company.lien = lien
        company.share_capital = share_capital
        company.other_facts = other_facts

        company.save()


        exec_time = time.time() - start
        print(f"Scraping completed in {exec_time} seconds")


def remove_html_and_tabs(text):
    return ' '.join(BeautifulSoup(text, "lxml").text.split())
