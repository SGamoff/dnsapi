from api.v1.views.management import *
from django.urls import path
from rest_framework import routers

app_name = 'v1'

urlpatterns = [
    path('service/', ServiceView.as_view(), name='service'),
    path('service/<int:pk>', ServiceIdView.as_view(), name='service_id'),
    path('zone/', ZoneView.as_view(), name='zone'),
    path('zone/<int:pk>', ZoneIdView.as_view(), name='zone_id'),
    path('zone/<int:pk>/import', ZoneImportByID.as_view(), name='zoneImportId'),
    path('zone/<int:pk>/export', ZoneExportByID.as_view(), name='zoneExportId'),
    path('zone/search/<str:pk>', ZoneDetailView.as_view(), name='zoneListId'),
    path('zone/<int:pk>/RR', ZoneResourceRecord.as_view(), name='zoneAddRR'),
]

