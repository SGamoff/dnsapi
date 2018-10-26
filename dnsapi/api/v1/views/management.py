import dns.zone
import dns.ipv4

from apps.editor.models import Service, Zone, RR
from apps.editor.serializers import ServiceSerilializers, ZoneSerilializers, RRSerilializers
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


class RRListView(ListAPIView):
    queryset = RR.objects.all()
    serializer_class = RRSerilializers


class RRCreateView(CreateAPIView):
    queryset = RR.objects.all()
    serializer_class = RRSerilializers


class RRUpdateView(UpdateAPIView):
    queryset = RR.objects.all()
    serializer_class = RRSerilializers


class RRRetrieveView(RetrieveAPIView):
    queryset = RR.objects.all()
    serializer_class = RRSerilializers


class RRDestroyView(DestroyAPIView):
    queryset = RR.objects.all()
    serializer_class = RRSerilializers


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
        try:
            findRR = RR.objects.filter(zone__exact=self.zone_name)
            # Clean all records before import from txt DANGEROUS
            if findRR.count() > 0:
                findRR.delete()
            zone = dns.zone.from_file(self.path, self.zone_name)
            findZone = Zone.objects.get(zone_name__exact=self.zone_name)
            result = ""
            for name, node in zone.nodes.items():
                for rdataset in node.rdatasets:
                    NewRR = RR.objects.create(recordName=name, textData=rdataset.to_text(), zone=findZone)
                    NewRR.save()
            return result
        except DNSException as e:
            return e.msg
        except ObjectDoesNotExist as e:
            return e.msg

    def export_zone_to_txt(self):
        try:
            findRR = RR.objects.filter(zone__exact=self.zone_name)
            if findRR.count()==0:
                return "Records not exists"
            exZone = dns.zone.Zone(self.zone_name)
            exNode = exZone.find_node(self.zone_name,True)
            newRdataset = exNode.rdatasets
            for rr in findRR:
                newRdataset.Rdataset.add(exZone, rr.textData)

                # newZone = exZone.find_node(rr.recordName,True)
                # newZone.get_rdataset(newRR.rdclass, newRR.rdtype, newRR.rdata, True)
            exZone.to_file(self.path)
        except DNSException as e:
            return e.msg