import django
from django.contrib.auth.models import User
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from docmanager.serializers import UserSerializer


class CurrentUserAPIView(APIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        print(request.user)
        try:
            queryset = User.objects.get(username=request.user)
            serializer = UserSerializer(queryset, many=False)
            return Response(serializer.data)
        except django.contrib.auth.models.User.DoesNotExist:
            return Response("User does not exist", status=status.HTTP_403_FORBIDDEN)

