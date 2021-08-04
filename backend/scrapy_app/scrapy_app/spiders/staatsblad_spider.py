import io
import json
import os
import re
import uuid

import lxml.html.clean
import requests
import scrapy
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from pdf2image import convert_from_path

from documents.models import Document, Page, Website

EXAMPLES = {
    "crosslang": "869914707",
    "colruyt": "400378485"
}

BASE_URL = 'http://www.ejustice.just.fgov.be/cgi_tsv/tsv_all.pl?DETAIL=ALL+PUB&lang=nl&btw='
QUERY_PARAMS = '&fromtab=TSV&sql=btw+contains+%27'
FILE_URL = 'http://www.ejustice.just.fgov.be'


class StaatsbladSpider(scrapy.Spider):
    name = 'Belgisch Staatsblad Publicaties'

    def start_requests(self):
        url = BASE_URL
        company_number = getattr(self, 'company_number', None)
        if company_number is not None:
            url = url + company_number + QUERY_PARAMS + company_number

        print("Started scraping for company number: ", company_number)
        print("Publications URL: ", url)
        yield scrapy.Request(url, self.parse_publications, meta={'download_timeout': 3600})

    def parse_publications(self, response):
        results = []

        # BeautifulSoup HTML Parser
        soup = BeautifulSoup(response.text, "html.parser")

        user = getattr(self, 'user', None)
        website = getattr(self, 'website', None)

        link_count = 0
        # Iterate over all <hr> tags (documents are separated with hr tags)
        for tag in soup.findAll():
            if tag.name == "hr":
                title = ""

                # If we found a <hr> tag, we search for the first <a> tag
                # but if another <hr> has been found instead, then we skip this one because it does not have any files.
                for sib in tag.next_siblings:
                    # A file has been found, we will do some cleanup, and add this to the results list
                    if sib.name == "a":
                        link_count = link_count + 1

                        title = tag.next_sibling
                        title_str = str(title)

                        # Sometimes a document number with a date is given,
                        # we want to catch this and add it to the title
                        if title.next_sibling is not None:
                            title_str = title_str + " - " + title.next_sibling.next_sibling

                        # Clean up, just for being sure. Encoding should handle this either way.
                        title_str = strip_html(clean_html(title_str))
                        title_str = title_str.replace("\u00a0", "").replace("\n", "")

                        # We take the href from the <a> sibling and append it to the base URL
                        url = FILE_URL + sib["href"]

                        print("TITLE: ", title_str)
                        print("URL  : ", url)

                        results.append({"title": title_str, "file": url})

                        # Create Document object in Django
                        user_obj = User.objects.get(username=user)
                        website_obj = Website.objects.get(name=website)
                        description = "Scraped from Belgisch Staatsblad Publicaties"
                        document = Document.objects.update_or_create(name=title_str,
                                                                     user=user_obj,
                                                                     website=website_obj,
                                                                     content=description)

                        doc = document[0]
                        print("Created document: ", doc.name)
                        print("id: ", doc.id)

                        res = requests.get(url)
                        # page = Page.objects.update_or_create(document=doc)

                        filename = "scraped_file.pdf"

                        with open(filename, 'wb+') as f:
                            f.write(res.content)

                            images = convert_from_path(filename)
                            print("images len: ", len(images))
                            for i in range(len(images)):
                                # Save pages as images in the pdf

                                image_name = f'scraped_file_{i}.jpg'
                                output_io = io.BytesIO()
                                images[i].save(output_io, 'JPEG')
                                output_io.name = image_name
                                image_hash = uuid.uuid4()

                                print("image_name: ", image_name)
                                print("output_io: ", output_io)
                                print("output_io.name: ", output_io.name)
                                print("images: ", images)
                                print("image_hash: ", image_hash)

                                page = Page.objects.update_or_create(image_hash=image_hash, defaults={'document': doc})
                                if page:
                                    page = page[0]
                                    print("Created page: ", page)
                                    page.update_image(output_io)
                                    print("Updated image: page looks like: ", page)

                        # os.remove(filename)

                        continue
                    if sib.name == "hr":
                        print("stopped, there is no link for this title")
                        break

                with open("kbo_publications.json", "w", encoding='utf8') as f:
                    json.dump(results, f, indent=8, ensure_ascii=False)

        print(f"Found {link_count} publications for this enterprise")


def strip_html(html):
    return clean_html(re.sub('<[^<]+?>', '', html.rstrip(os.linesep)))


def clean_html(html):
    doc = lxml.html.fromstring(html)
    cleaner = lxml.html.clean.Cleaner(style=True)
    doc = cleaner.clean_html(doc)
    return doc.text_content()
