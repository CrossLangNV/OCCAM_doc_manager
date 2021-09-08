import io
import time
import uuid

import requests
import scrapy
from bs4 import BeautifulSoup
from pdf2image import convert_from_path
from scrapy import Selector

from ctr.models import CtrCompany
from django.contrib.auth.models import User

from documents.models import Website, LayoutAnalysisModel, Document, Page

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

DIGITAL_FILE = "Digitální podoba:"
FINANCIAL_STATEMENT = "účetní závěrka"

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
        yield scrapy.Request(url, self.parse_ctr_company_information)

    def parse_ctr_company_information(self, response):
        start = time.time()

        identification_number = str(self.company_number).strip()
        print(f"Started 'CTR Company Information Extraction' extraction for company number: {identification_number}")

        try:
            company = CtrCompany.objects.get(identification_number=identification_number)
        except CtrCompany.DoesNotExist:
            company = CtrCompany.objects.create(identification_number=identification_number)

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

                    # Skip first here because the first one is the type
                    values = []
                    for value in sib.find_all("div", class_="div-cell")[1:]:
                        if not value.get_text().startswith("zapsáno"):
                            values.append(remove_html_and_tabs(value.get_text()))

                    values_str = "\n".join(values)

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
        print(f"Scraping company information completed in {exec_time} seconds")

        company_number = getattr(self, 'company_number', None)
        publications_url = LEGAL_DOCUMENTS_URL + company_number
        yield scrapy.Request(publications_url, self.parse_ctr_publications)

    def parse_ctr_publications(self, response):
        start = time.time()

        identification_number = str(self.company_number).strip()
        user = getattr(self, 'user', None)
        website = getattr(self, 'website', None)

        print(f"Started 'CTR Company Publications' extraction for company number: {identification_number}")

        rows = response.xpath('//table[@class="list"]/tbody/tr')

        for row in rows:
            document_number = row.xpath('td[1]//span/text()').extract_first()
            document_url = "https://or.justice.cz/ias/ui/" + str(row.xpath('td[1]//a/@href').extract_first())[2:]
            document_type = row.xpath('td[2]//span//span/text()').extract_first()
            origin_of_the_document = row.xpath('td[3]/text()').extract_first()

            digitized_status = row.xpath('td[7]//span/@title').extract()[0]

            print("document_number: ", document_number)
            print("document_url: ", document_url)
            print("document_type: ", document_type)
            print("origin_of_the_document: ", origin_of_the_document)
            print("digitized_status: ", digitized_status)

            document_name = document_number + " - " + document_type
            print("document_name: ", document_name)

            # TODO: Create the document and all its information.

            # Create Document object in Django
            if user == "demo":
                user_obj = None
            else:
                user_obj = User.objects.get(username=user)

            website_obj = Website.objects.get(name=website)
            description = "Scraped from Czech Business Register"

            layout_model = LayoutAnalysisModel.objects.get(name="Czech old printed")
            document = Document.objects.update_or_create(name=document_name,
                                                         user=user_obj,
                                                         website=website_obj,
                                                         content=description,
                                                         layout_analysis_model=layout_model)

            doc = document[0]
            print("Created/updated document: ", doc.name)
            print("id: ", doc.id)



            yield scrapy.Request(document_url, self.parse_download_file, meta={
                "doc_id": doc.id,
                "doc_url": document_url,
            })


        exec_time = time.time() - start
        print(f"Scraping publications completed in {exec_time} seconds")

    def parse_download_file(self, response):
        start = time.time()
        doc_id = response.meta.get("doc_id")
        doc_url = response.meta.get("doc_url")

        print("Downloading file for document id: ", doc_id)
        print(doc_url)

        doc = Document.objects.get(pk=doc_id)

        # GET THE DOWNLOADABLE URL
        rows = response.xpath('//table/tbody/tr')

        for row in rows:
            table_item_type = row.xpath('th/text()').extract_first()

            if table_item_type == DIGITAL_FILE:
                file = "https://or.justice.cz" + row.xpath('td//a/@href').extract_first()
                print("file url: ", file)

        res = requests.get(file)
        filename = "scraped_file.pdf"

        with open(filename, 'wb+') as f:
            f.write(res.content)

            images = convert_from_path(filename)
            for i in range(len(images)):
                # Save pages as images in the pdf
                image_name = f'scraped_file_{i}.jpg'
                output_io = io.BytesIO()
                images[i].save(output_io, 'JPEG')
                output_io.name = image_name
                image_hash = uuid.uuid4()

                page = Page.objects.update_or_create(image_hash=image_hash, defaults={'document': doc})
                if page:
                    page = page[0]
                    print("Created page: ", page)
                    page.update_image(output_io)
                    print("Updated image: page looks like: ", page)



        exec_time = time.time() - start
        print(f"Downloading files completed in {exec_time} seconds")


def remove_html_and_tabs(text):
    return ' '.join(BeautifulSoup(text, "lxml").text.split())
