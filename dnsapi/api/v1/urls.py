from api.v1.views.management import *
from django.urls import path

app_name = 'v1'

urlpatterns = [
    path('service/list', ServiceListView.as_view(), name='serviceList'),
    path('service/add', ServiceCreateView.as_view(), name='serviceAdd'),
    path('service/update', ServiceUpdateView.as_view(), name='serviceUpdate'),
    path('service/retrieve', ServiceRetrieveView.as_view(), name='serviceRetrieve'),
    path('service/del', ServiceDestroyView.as_view(), name='serviceDel'),
    path('zone/list', ZoneListView.as_view(), name='zoneList'),
    path('zone/add', ZoneCreateView.as_view(), name='zoneAdd'),
    path('zone/update', ZoneUpdateView.as_view(), name='zoneUpdate'),
    path('zone/retrieve', ZoneRetrieveView.as_view(), name='zoneRetrieve'),
    path('zone/del', ZoneDestroyView.as_view(), name='zoneDel'),
    path('zone/load', load_zone_file, name="zoneLoad"),
    path('zone/export', export_zone, name='zoneExport'),
]

