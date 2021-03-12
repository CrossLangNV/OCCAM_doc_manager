from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions

from leads.models import Lead
from leads.serializers import LeadSerializer


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = LeadSerializer
