from django.urls import path

from tutorial.views import UserTutorialAPIView

urlpatterns = [
    path("api/usertutorials", UserTutorialAPIView.as_view(), name="user_tutorials_api_detail"),
]
