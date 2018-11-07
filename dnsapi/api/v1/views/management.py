import dns.zone
import dns.ipv4

from apps.editor.models import Service, Zone
from apps.editor.serializers import ServiceSerilializers, ZoneSerilializers
from datetime import date
from dns.exception import DNSException
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets


class ServiceView(viewsets.ModelViewSet):
    """
    A router for API Service GET, PUT, PATCH, DELETE, HEAD, OPTIONS
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerilializers
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ZoneView(viewsets.ModelViewSet):
    """
    A router for API Zone GET, PUT, PATCH, DELETE, HEAD, OPTIONS
    """
    queryset = Zone.objects.all()
    serializer_class = ZoneSerilializers
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ZoneImportByID(APIView):
    """
    A router for API Zone import by ID POST
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    @staticmethod
    def get_object(pk):
        try:
            return Zone.objects.get(zone_id=pk)
        except Zone.DoesNotExist:
            raise Http404

    def post(self, request, pk):
        zone_obj = self.get_object(pk)
        zone_import = ZoneOperations(zone_obj.path_file, zone_obj.zone_name)
        return Response({"message": str(zone_import.read_zone_from_txt())})


class ZoneExportByID(APIView):
    """
    A router for API Zone export by ID POST
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    @staticmethod
    def get_object(pk):
        try:
            return Zone.objects.get(zone_id=pk)
        except Zone.DoesNotExist:
            raise Http404

    def post(self, request, pk):
        zone_obj = self.get_object(pk)
        zone_export = ZoneOperations(zone_obj.path_file, zone_obj.zone_name)
        return Response({"message": str(zone_export.export_zone_to_txt())})


class ZoneResourceRecord(APIView):
    """
    A router for API Zone resource records operations by zone ID POST
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    @staticmethod
    def get_object(pk):
        try:
            return Zone.objects.get(zone_id=pk)
        except Zone.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        rr_text = self.get_object(pk)
        find_record = ResourceRecordOperations(rr_text.zone_id)
        return Response(str(find_record.find_and_return_records()))

    def put(self, request, pk):
        zone_obj = self.get_object(pk)
        zone_add_rr = ZoneOperations(zone_obj.path_file, zone_obj.zone_name)
        return Response({"message": str(zone_add_rr.add_resource_record(request))})

    def post(self, request, pk):
        zoneObj = self.get_object(pk)
        ZoneDeleteRR = ZoneOperations(zoneObj.path_file, zoneObj.zone_name)
        return Response({"message": str(ZoneDeleteRR.del_resource_record(request))})


class ZoneDetailView(APIView):

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    @staticmethod
    def get_object(pk):
        try:
            return Zone.objects.get(zone_name__exact=pk)
        except Zone.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        zone = self.get_object(pk)
        serializer = ZoneSerilializers(zone)
        return Response(serializer.data)


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
            find_zone = Zone.objects.get(zone_name__exact=self.zone_name)
            result = ""
            reload_zone_to_db = True
            if len(find_zone.zone_text) > 0:
                # return findZone.zone_text
                old_zone = dns.zone.from_text(find_zone.zone_text.replace("\r", ""), self.zone_name)
                if old_zone == zone:
                    result = "Update zone success! Nothing to do"
                    reload_zone_to_db = False
                else:
                    find_zone.zone_text = ""
            if reload_zone_to_db:
                with open(self.path, "r") as f:
                    lines = f.read()
                    find_zone.zone_text = lines
                    find_zone.save()
                result = "New zone has been loaded!"
            return result
        except DNSException as e:
            return e.msg
        except ObjectDoesNotExist as e:
            return e

    def export_zone_to_txt(self):
        """
        export zone from database if was changed
        :return:
        result: str
        """
        try:
            old_zone = dns.zone.from_file(self.path, self.zone_name)
            find_zone = Zone.objects.get(zone_name__exact=self.zone_name)
            result = ""
            if len(find_zone.zone_text) > 0:
                new_zone = dns.zone.from_text(find_zone.zone_text.replace("\r", ""), self.zone_name)
                if old_zone == new_zone:
                    result = "Nothing export to file"
                else:
                    new_zone.to_file(self.path)
                    result = "Zone has been exported to file"
            return result
        except DNSException as e:
            return e.msg
        except OSError as e:
            return e

    def add_resource_record(self, request):
        try:
            find_zone = Zone.objects.get(zone_name__exact=self.zone_name)
            mod_zone = ''
            serial = ''
            if len(find_zone.zone_text) > 0:
                mod_zone = dns.zone.from_text(find_zone.zone_text.replace("\r", ""), self.zone_name)
            default_ttl = dns.ttl.from_text("0")
            for (name, ttl, rdata) in mod_zone.iterate_rdatas('SOA'):
                serial = self._generate_serial(rdata.serial)
                default_ttl = str(ttl)
                rdata.serial = serial
            rr_ttl = dns.ttl.from_text(request.data.get("rrttl", default_ttl))
            rr_type = dns.rdatatype.from_text(request.data.get("rrtype"))
            origin_name = dns.name.from_text(self.zone_name)
            rr_name = dns.name.from_text(request.data.get("rrname", "@"), origin_name)
            rr_class = dns.rdataclass.from_text(request.data.get("rrclass", "IN"))
            rr_dataset = mod_zone.find_rdataset(rr_name, rr_type, create=True)
            rr_text = request.data.get("rrtext", None)
            rr_data = dns.rdata.from_text(rr_class, rr_type, rr_text)
            rr_dataset.add(rr_data, rr_ttl)
            find_zone.zone_text = mod_zone.to_text().decode('utf-8')
            find_zone.save()
            result = "Zone with serial number {} was created".format(serial)
        except DNSException as e:
            return e.msg
        return result

    def del_resource_record(self, request):
        result = ""
        try:
            find_zone = Zone.objects.get(zone_name__exact=self.zone_name)
            mod_zone = ''
            serial = ''
            if len(find_zone.zone_text) > 0:
                mod_zone = dns.zone.from_text(find_zone.zone_text.replace("\r", ""), self.zone_name)
            for (name, ttl, rdata) in mod_zone.iterate_rdatas('SOA'):
                serial = self._generate_serial(rdata.serial)
                rdata.serial = serial
            rr_type = dns.rdatatype.from_text(request.data.get("rrtype"))
            origin_name = dns.name.from_text(self.zone_name)
            rr_name = dns.name.from_text(request.data.get("rrname", "@"), origin_name)
            mod_zone.delete_rdataset(rr_name, rr_type)
            find_zone.zone_text = mod_zone.to_text().decode('utf-8')
            find_zone.save()
            result = "Zone with serial number {} was updated".format(serial)
        except DNSException as e:
            return e.msg
        return result

    @staticmethod
    def _generate_serial(old_serial):
        new_serial = date.today().strftime("%Y%m%d")
        old_serial = str(old_serial)
        if len(old_serial) < 10 or len(old_serial) != 10 or old_serial[:8] != new_serial:
            new_serial += "01"
        elif old_serial[:8] == new_serial:
            delta = str(int(old_serial[-2::]) + 1)
            if len(delta) < 2:
                delta = "0" + delta
            new_serial = old_serial[:8] + delta
        return int(new_serial)


class ResourceRecordOperations():

    def __init__(self, zone_id):
        self.zone_id = zone_id

    def find_and_return_records(self):
        result = {}
        try:
            find_zone = Zone.objects.get(zone_id__exact=self.zone_id)
            zone_rdatasets = ""
            if len(find_zone.zone_text) > 0:
                zone_rdatasets = dns.zone.from_text(find_zone.zone_text.replace("\r", ""), find_zone.zone_name)
            for rr_dataset in zone_rdatasets:
                for rr_data in rr_dataset:
                    result[rr_data.decode('utf-8')] = ""
        except DNSException as e:
            return e.msg
        return result
