import dns.zone
import dns.ipv4

from apps.editor.models import Service, Zone
from apps.editor.serializers import ServiceSerilializers, ZoneSerilializers
from datetime import date
from dns.exception import  DNSException
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, \
        RetrieveAPIView, DestroyAPIView
from rest_framework.views import APIView
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


class ZoneImportByID(APIView):

    def get_object(self, pk):
        try:
            return Zone.objects.get(service = pk)
        except Zone.DoesNotExist:
            raise Http404

    def post(self,request, pk):
        zoneObj = self.get_object(pk)
        zoneImport = ZoneOperations(zoneObj.path_file, zoneObj.zone_name)
        return Response({"message": str(zoneImport.read_zone_from_txt())})

class ZoneExportByID(APIView):

    def get_object(self, pk):
        try:
            return Zone.objects.get(service = pk)
        except Zone.DoesNotExist:
            raise Http404

    def post(self,request, pk):
        zoneObj = self.get_object(pk)
        zoneExport = ZoneOperations(zoneObj.path_file, zoneObj.zone_name)
        return Response({"message": str(zoneExport.export_zone_to_txt())})


class ZoneResourceRecord(APIView):

    def get_object(self, pk):
        try:
            return Zone.objects.get(service = pk)
        except Zone.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        zoneObj = self.get_object(pk)
        ZoneAddRR = ZoneOperations(zoneObj.path_file, zoneObj.zone_name)
        return Response({"message": str(ZoneAddRR.add_resource_record(request))})

    def delete(self, request, pk):
        zoneObj = self.get_object(pk)
        ZoneDeleteRR = ZoneOperations(zoneObj.path_file, zoneObj.zone_name)
        return Response({"message": str(ZoneDeleteRR.del_resource_record(request))})


class ZoneDetailView(APIView):

    def get_object(self, pk):
        try:
            return Zone.objects.get(zone_name__exact = pk)
        except Zone.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        zone = self.get_object(pk)
        serializer = ZoneSerilializers(zone)
        return Response(serializer.data)


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

    def add_resource_record(self, request):
        result = ""
        try:
            # result = dns.rdatatype.from_text(request.data.get("rrtype"))
            findZone = Zone.objects.get(zone_name__exact=self.zone_name)
            if len(findZone.zone_text) > 0:
                modZone = dns.zone.from_text(findZone.zone_text.replace("\r", ""), self.zone_name)
            default_ttl = dns.ttl.from_text("0")
            for (name, ttl, rdata) in modZone.iterate_rdatas('SOA'):
                serial = self._generate_serial(rdata.serial)
                default_ttl = str(ttl)
                rdata.serial = serial
            rrttl = dns.ttl.from_text(request.data.get("rrttl", default_ttl))
            rrtype = dns.rdatatype.from_text(request.data.get("rrtype"))
            originname = dns.name.from_text(self.zone_name)
            rrname = dns.name.from_text(request.data.get("rrname", "@"), originname)
            rrclass = dns.rdataclass.from_text(request.data.get("rrclass", "IN"))
            rrdataset = modZone.find_rdataset(rrname, rrtype, create=True)
            rrtext = request.data.get("rrtext", None)
            rrdata = dns.rdata.from_text(rrclass, rrtype, rrtext)
            rrdataset.add(rrdata, rrttl)
            findZone.zone_text = modZone.to_text().decode('utf-8')
            findZone.save()
            result = "Zone with serial number {} was created".format(serial)
        except DNSException as e:
            return e.msg
        return result

    def del_resource_record(self, request):
        result = ""
        try:
            findZone = Zone.objects.get(zone_name__exact=self.zone_name)
            if len(findZone.zone_text) > 0:
                modZone = dns.zone.from_text(findZone.zone_text.replace("\r", ""), self.zone_name)
            for (name, ttl, rdata) in modZone.iterate_rdatas('SOA'):
                serial = self._generate_serial(rdata.serial)
                rdata.serial = serial
            rrtype = dns.rdatatype.from_text(request.data.get("rrtype"))
            originname = dns.name.from_text(self.zone_name)
            rrname = dns.name.from_text(request.data.get("rrname", "@"), originname)
            modZone.delete_rdataset(rrname, rrtype)
            findZone.zone_text = modZone.to_text().decode('utf-8')
            findZone.save()
            result = "Zone with serial number {} was updated".format(serial)
        except DNSException as e:
            return e.msg
        return result

    def _generate_serial(self, oldserial):
        newserial = date.today().strftime("%Y%m%d")
        oldserial = str(oldserial)
        if len(oldserial) < 10 or len(oldserial) != 10 or oldserial[:8] != newserial:
            newserial += "01"
        elif oldserial[:8] == newserial:
            delta = str(int(oldserial[-2::]) + 1)
            if len(delta) < 2:
                delta = "0" + delta
            newserial = oldserial[:8] + delta
        return int(newserial)
    # def del_resource_record(self, request):
