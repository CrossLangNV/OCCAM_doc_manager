import os

from scrapyd_api import ScrapydAPI

from scheduler.celery import app

scrapyd = ScrapydAPI(os.environ["SCRAPYD_URL"])


@app.task(rate_limit='30/m')
def launch_scrapyd_throttled_request(website, settings, enterprise_number, user, *args, **kwargs):
    task = scrapyd.schedule('default', website, settings=settings,
                            company_number=enterprise_number,
                            user=user, website=website)
