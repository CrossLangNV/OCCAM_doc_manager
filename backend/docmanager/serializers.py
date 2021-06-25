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
        user_tutorial = UserTutorial.objects.get(user=user)
        if user_tutorial:
            return user_tutorial.has_completed
        else:
            return True

    class Meta:
        model = User
        exclude = ["password"]
