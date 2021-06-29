from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from tutorial.models import UserTutorial
from tutorial.serializers import UserTutorialSerializer


class UserTutorialAPIView(APIView):
    queryset = UserTutorial.objects.all()
    serializer_class = UserTutorialSerializer

    def post(self, request):
        user_email = request.data["user"]
        value = request.data["value"]
        user = User.objects.get(email=user_email)

        print("user_email: ", user_email)
        print("value: ", value)
        if value:
            UserTutorial.objects.filter(user=user).update(has_completed=True)
        else:
            UserTutorial.objects.filter(user=user).update(has_completed=False)

        return Response("", HTTP_200_OK)
