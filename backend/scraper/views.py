import logging
import os
from uuid import uuid4

import requests.exceptions
from django.http.response import JsonResponse
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from scrapyd_api import ScrapydAPI

from scraper.models import ScrapyItem

# connect scrapyd service
scrapyd = ScrapydAPI(os.environ["SCRAPYD_URL"])

logger = logging.getLogger(__name__)


class LaunchScraperAPIView(APIView):
    queryset = ScrapyItem.objects.none()
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            website = request.data["website"]
            company_number = request.data["company_number"]
            user = request.data["user"]

            unique_id = str(uuid4())  # create a unique ID.
            settings = {
                'unique_id': unique_id,  # unique ID for each record for DB
                'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
            }

            task = scrapyd.schedule('default', website, settings=settings,
                                    company_number=company_number, user=user, website=website)

            response = {
                "message": "Started scraper task",
                "task_id": task,
                "company_number": company_number,
                "website": website,
                "user": user
            }

            return Response(response,
                            status=status.HTTP_201_CREATED)
        except KeyError as e:
            return Response("Invalid request format. Please specify both 'website', 'user' and 'company_number' keys.",
                            status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.ConnectionError as e:
            logger.error(e)
            return Response("Failed to connect to the scrapyd service.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        task_id = request.GET.get('task_id', None)
        unique_id = request.GET.get('unique_id', None)

        if not task_id or not unique_id:
            return JsonResponse({'error': 'Missing args'})

            # Here we check status of crawling that just started a few seconds ago.
            # If it is finished, we can query from database and get results
            # If it is not finished we can return active status
            # Possible results are -> pending, running, finished
            status = scrapyd.job_status('default', task_id)
            if status == 'finished':
                try:
                    # this is the unique_id that we created even before crawling started.
                    item = ScrapyItem.objects.get(unique_id=unique_id)
                    return JsonResponse({'data': item.to_dict['data']})
                except Exception as e:
                    return JsonResponse({'error': str(e)})
            else:
                return JsonResponse({'status': status})
