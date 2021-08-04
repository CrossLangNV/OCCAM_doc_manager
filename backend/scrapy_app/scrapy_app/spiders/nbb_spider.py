import scrapy

EXAMPLES = {
    "crosslang": "869914707",
    "colruyt": "400378485"
}

BASE_URL = 'http://cri.nbb.be/bc9/web/catalog?lang=N&companyNr='


class StaatsbladSpider(scrapy.Spider):
    name = 'NBB'

    def start_requests(self):
        url = BASE_URL
        company_number = getattr(self, 'company_number', None)
        if company_number is not None:
            url = url + company_number

        print(f"Started '{self.name}' scraper for company number: ", company_number)
        print("Publications URL: ", url)
        yield scrapy.Request(url, self.parse_nbb_publications)

    def parse_nbb_publications(self, response):
        print("Started scrapy 'parse_nbb_publications' request")
        print("Not implemented yet.")

        print("Response text: ", response.text)

        rows = response.xpath('//table[@class="baseDataTable"]/tbody/tr')
        for row in rows:
            td1 = row.xpath('td[1]/text()').extract_first()
            td2 = row.xpath('td[2]/text()').extract_first()
            print("td1: ", td1)
            print("td2: ", td2)
