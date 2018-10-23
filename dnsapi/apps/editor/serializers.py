from rest_framework import serializers
from .models import Service, Zone, RR


class ServiceSerilializers(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ("name", "port", "server_type")


class ZoneSerilializers(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ("path_file", "zone_name", "zone_type", "service")


class RRSerilializers(serializers.ModelSerializer):
    class Meta:
        model = RR
        fields = ("name", "ttl", "rc", "rr", "rd", "zone")