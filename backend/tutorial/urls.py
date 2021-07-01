from django.urls import path

from tutorial.views import UserTutorialAPIView, HelpPageAPIView

urlpatterns = [
    path("api/usertutorials", UserTutorialAPIView.as_view(), name="user_tutorials_api_detail"),
    path("api/help_page", HelpPageAPIView.as_view(), name="help_page_api"),
]
