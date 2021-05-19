from rest_framework import serializers

from activitylogs.models import ActivityLog


class ActivityLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActivityLog
        fields = "__all__"
        depth = 2
