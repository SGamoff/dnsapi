from rest_framework import serializers
from apps.editor.models import Service, Zone


class ServiceSerilializers(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('service_id', 'name', 'port', 'server_type')


class ZoneSerilializers(serializers.ModelSerializer):

    class Meta:
        model = Zone
        fields = ('zone_id', 'path_file', 'zone_name',
                  'zone_type', 'zone_text', 'service')
