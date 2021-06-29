from rest_framework import serializers

from tutorial.models import UserTutorial


class UserTutorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTutorial
        fields = "__all__"
