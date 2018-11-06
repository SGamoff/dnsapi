from api.v1.views.management import *
from django.urls import path
from rest_framework import routers

app_name = 'v1'

router = routers.DefaultRouter()
router.register(r'service', ServiceView, base_name='service')
router.register(r'zone', ZoneView, base_name='zone')

urlpatterns = [
    path('zone/<int:pk>/import', ZoneImportByID.as_view(), name='zone_import_id'),
    path('zone/<int:pk>/export', ZoneExportByID.as_view(), name='zone_export_id'),
    path('zone/search/<str:pk>', ZoneDetailView.as_view(), name='zone_list_id'),
    path('zone/<int:pk>/RR', ZoneResourceRecord.as_view(), name='zone_add_rr'),
]

urlpatterns += router.urls
