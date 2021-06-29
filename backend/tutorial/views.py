import os

from atlassian import Confluence
from django.contrib.auth.models import User
from rest_framework import permissions
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

        if value:
            UserTutorial.objects.filter(user=user).update(has_completed=True)
        else:
            UserTutorial.objects.filter(user=user).update(has_completed=False)

        return Response("", HTTP_200_OK)


class HelpPageAPIView(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        confluence = Confluence(
            url=os.environ['CONFLUENCE_URL'],
            username=os.environ['CONFLUENCE_USERNAME'],
            password=os.environ['CONFLUENCE_PASSWORD'])

        page = confluence.get_page_by_title(os.environ['CONFLUENCE_SPACE'], os.environ['CONFLUENCE_MANUAL_PAGE_TITLE'],
                                            expand='body.storage')

        page_id = page['id']
        content = page['body']['storage']['value']

        return Response(content, HTTP_200_OK)
