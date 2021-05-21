from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination

from activitylogs.models import ActivityLog
from activitylogs.serializers import ActivityLogSerializer


class SmallResultsSetPagination(LimitOffsetPagination):
    default_limit = 5
    limit_query_param = "rows"
    offset_query_param = "offset"


class ActivityLogsAPIView(ListCreateAPIView):
    queryset = ActivityLog.objects.all()
    pagination_class = SmallResultsSetPagination
    serializer_class = ActivityLogSerializer

    def get_queryset(self):
        q = ActivityLog.objects.all()
        page_id = self.request.GET.get("page", "")
        overlay_id = self.request.GET.get("overlay", "")

        if page_id:
            q = q.filter(page__id=str(page_id))

        if overlay_id:
            q = q.filter(overlay_id=str(overlay_id))

        return q


class ActivityLogsDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
