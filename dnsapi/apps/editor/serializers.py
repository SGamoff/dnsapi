from rest_framework import serializers
from .models import Service, Zone


from apps.editor.emums import ZoneTypes, ServerTypes


class ServiceSerilializers(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ("name", "port", "server_type")


class ZoneSerilializers(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    # path_file = serializers.CharField(max_length=4096)
    # zone_name = serializers.CharField(required=True, max_length=255)
    # zone_type = serializers.ChoiceField(default=ZoneTypes.FWD,
    #                              choices=ZoneTypes.Choices)
    # zone_text = serializers.CharField(required=False)
    # service = serializers.RelatedField(source='service', read_only=True)

    class Meta:
        model = Zone
        fields = ("path_file", "zone_name", "zone_type", "zone_text", "service")
