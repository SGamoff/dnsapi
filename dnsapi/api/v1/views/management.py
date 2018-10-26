import dns.zone
import dns.ipv4
import sys

from apps.editor.models import Service, Zone
from apps.editor.serializers import ServiceSerilializers, ZoneSerilializers
from dns.exception import  DNSException
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, \
        RetrieveAPIView, DestroyAPIView
from rest_framework.response import Response


class ServiceListView(ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerilializers


class ServiceCreateView(CreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerilializers


class ServiceUpdateView(UpdateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerilializers


class ServiceRetrieveView(RetrieveAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerilializers


class ServiceDestroyView(DestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerilializers


class ZoneListView(ListAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerilializers


class ZoneCreateView(CreateAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerilializers


class ZoneUpdateView(UpdateAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerilializers


class ZoneRetrieveView(RetrieveAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerilializers


class ZoneDestroyView(DestroyAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerilializers


@api_view(['GET'])
def load_zone_file(request):
    if request.method == "GET":
        getZone = ZoneOperations("/home/gsv/PycharmProjects/dnsapi/docker/conf/localhost.zone", "localhost")
        return Response({"message": str(getZone.read_zone_from_txt())})
    Response({"message": "Only GET method supported"})

@api_view(['GET'])
def export_zone(request):
    if request.method == "GET":
        setZone = ZoneOperations("/home/gsv/PycharmProjects/dnsapi/docker/conf/localhost1.zone","localhost")
        return Response({"message": str(setZone.export_zone_to_txt())})
    Response({"message": "Only GET method supported"})


class ZoneOperations():

    def __init__(self, path, zone_name):
        self.path = path
        self.zone_name = zone_name

    def read_zone_from_txt(self):
        """
        load zone from bind format file in DB if need update
        :return:
        result: str
        """
        try:
            zone = dns.zone.from_file(self.path, self.zone_name)
            findZone = Zone.objects.get(zone_name__exact=self.zone_name)
            result = ""
            reload_zone_to_db = True
            if len(findZone.zone_text) > 0:
                # return findZone.zone_text
                oldzone = dns.zone.from_text(findZone.zone_text.replace("\r",""),self.zone_name)
                if oldzone == zone:
                    result = "Update zone success! Nothing to do"
                    reload_zone_to_db = False
                else:
                    findZone.zone_text=""
            if reload_zone_to_db:
                with open(self.path,"r") as f:
                    lines = f.read()
                    findZone.zone_text = lines
                    findZone.save()
                result = "New zone has been loaded!"
            return result
        except DNSException as e:
            return e.msg
        except ObjectDoesNotExist as e:
            return e.msg

    def export_zone_to_txt(self):
        """
        export zone from database if was changed
        :return:
        result: str
        """
        try:
            oldZone = dns.zone.from_file(self.path, self.zone_name)
            findZone = Zone.objects.get(zone_name__exact=self.zone_name)
            result = ""
            if len(findZone.zone_text) > 0:
                newZone = dns.zone.from_text(findZone.zone_text.replace("\r",""), self.zone_name)
                if oldZone == newZone:
                    result = "Nothing export to file"
                else:
                    newZone.to_file(self.path)
                    result = "Zone has been exported to file"
            return result
        except DNSException as e:
            return e.msg
        except OSError as e:
            return e.msg