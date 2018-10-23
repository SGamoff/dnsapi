from django.urls import path
from django.conf.urls import include

app_name = 'api'

urlpatterns = [
    path('v1/', include('api.v1.urls', namespace='v1')),

]

