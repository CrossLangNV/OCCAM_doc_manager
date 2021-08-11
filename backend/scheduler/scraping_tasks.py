import csv
import os

from scrapyd_api import ScrapydAPI

from scheduler.celery import app

scrapyd = ScrapydAPI(os.environ["SCRAPYD_URL"])

"""
    - With 1.5 million records:
        - Rate limit of 240/m takes 10.5 days  
        - Rate limit of 120/m takes 21 days  
        - Rate limit of 60/m takes 42 days  
"""


@app.task(rate_limit='60/m')
def launch_scrapyd_throttled_staatsblad(website, settings, user, limit, *args, **kwargs):
    with open(os.environ["ENTERPRISES_FILE_PATH"], "r") as csvfile:
        csv_reader = csv.reader(csvfile)

        count = 0

        for row in reversed(list(csv_reader)):

            # Launch scraper for every record in the Staatsblad companies CSV file
            enterprise_number = row[0]

            if enterprise_number != "EnterpriseNumber":
                enterprise_number = enterprise_number.replace(".", "")
                print(f"Started scraping for enterprise number: {enterprise_number} (#{count})")

                task = scrapyd.schedule('default', website, settings=settings,
                                        company_number=enterprise_number,
                                        user=user, website=website)

                if limit and count == limit:
                    break

            count = count + 1
