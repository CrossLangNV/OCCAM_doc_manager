from django.urls import path

from activitylogs.views import ActivityLogsAPIView, ActivityLogsDetailAPIView

urlpatterns = [
    path('api/activitylogs', ActivityLogsAPIView.as_view(), name='activity_logs_api_list'),
    path("api/activitylogs/<str:pk>", ActivityLogsDetailAPIView.as_view(), name="activity_logs_api_detail"),
]
