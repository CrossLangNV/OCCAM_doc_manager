from django.urls import path

from scraper.views import LaunchScraperAPIView

urlpatterns = [
    path("api/launch_scraper", LaunchScraperAPIView.as_view(), name="launch_scraper_api"),
]
