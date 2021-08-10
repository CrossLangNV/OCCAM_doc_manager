import os

from celery import shared_task
from scrapyd_api import ScrapydAPI

scrapyd = ScrapydAPI(os.environ["SCRAPYD_URL"])


@shared_task
def launch_scrapyd_throttled_request(website, settings, enterprise_number, user, *args, **kwargs):
    task = scrapyd.schedule('default', website, settings=settings,
                            company_number=enterprise_number,
                            user=user, website=website)
