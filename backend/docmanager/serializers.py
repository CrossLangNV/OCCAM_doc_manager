from django.contrib.auth.models import User, Group
from rest_framework import serializers

from tutorial.models import UserTutorial


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["name"]


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    has_completed = serializers.SerializerMethodField()

    def get_has_completed(self, user):
        try:
            user_tutorial = UserTutorial.objects.get(user=user)
            return user_tutorial.has_completed

        except UserTutorial.DoesNotExist:
            user_tutorial = UserTutorial.objects.create(user=user)
            return user_tutorial.has_completed

    class Meta:
        model = User
        exclude = ["password"]
