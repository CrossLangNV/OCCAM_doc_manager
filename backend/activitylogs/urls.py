from django.urls import path

from activitylogs.views import ActivityLogsAPIView, ActivityLogsDetailAPIView

urlpatterns = [
    path('api/activity_logs', ActivityLogsAPIView.as_view(), name='activity_logs_api_list'),
    path("api/activity_logs/<str:pk>", ActivityLogsDetailAPIView.as_view(), name="activity_logs_api_detail"),
]
