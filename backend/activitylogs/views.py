from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination

from activitylogs.models import ActivityLog
from activitylogs.serializers import ActivityLogSerializer
from documents.models import Overlay


class SmallResultsSetPagination(LimitOffsetPagination):
    default_limit = 5
    limit_query_param = "rows"
    offset_query_param = "offset"


class ActivityLogsAPIView(ListCreateAPIView):
    queryset = ActivityLog.objects.all()
    pagination_class = SmallResultsSetPagination
    serializer_class = ActivityLogSerializer

    def get_queryset(self):
        q = ActivityLog.objects.filter(user=self.request.user)
        page_id = self.request.GET.get("page", "")
        overlay_id = self.request.GET.get("overlay", "")
        type = self.request.GET.get("type", "")
        only_latest = self.request.GET.get("onlyLatest", "")

        # if 1, also show history of overlays linked to a page
        linked_overlays = self.request.GET.get("linked_overlays", "")

        if page_id:
            q = q.filter(page__id=str(page_id))
            if linked_overlays:
                overlays = Overlay.objects.filter(page__id=page_id)

                q = q.filter(overlay__in=list(overlays))

        if overlay_id:
            q = q.filter(overlay_id=str(overlay_id))

        if type:
            q = q.filter(type=str(type))

        if only_latest == "true":
            q = q.latest('created_at')

        return q


class ActivityLogsDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
