from rest_framework import serializers

from activitylogs.models import ActivityLog


class ActivityLogSerializer(serializers.ModelSerializer):
    # page = serializers.PrimaryKeyRelatedField(queryset=Page.objects.all())

    class Meta:
        model = ActivityLog
        fields = "__all__"
