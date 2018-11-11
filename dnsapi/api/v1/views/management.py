from api.v1.serializers import ServiceSerilializers, ZoneSerilializers
from api.v1.utils.zoneoperations import ZoneOperations, \
    ResourceRecordOperations
from apps.editor.models import Service, Zone
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import viewsets


class ServiceView(viewsets.ModelViewSet):
    '''
    A router for API Service GET, PUT, PATCH, DELETE, HEAD, OPTIONS
    '''
    queryset = Service.objects.all()
    serializer_class = ServiceSerilializers
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ZoneView(viewsets.ModelViewSet):
    '''
    A router for API Zone GET, PUT, PATCH, DELETE, HEAD, OPTIONS
    '''
    queryset = Zone.objects.all()
    serializer_class = ZoneSerilializers
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ZoneImportByID(APIView):
    '''
    A router for API Zone import by ID POST
    '''
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
        return Response({'message': str(zone_import.read_zone_from_txt())})


class ZoneExportByID(APIView):
    '''
    A router for API Zone export by ID POST
    '''
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
        return Response({'message': str(zone_export.export_zone_to_txt())})


class ZoneResourceRecord(APIView):
    '''
    A router for API Zone resource records operations by zone ID POST
    '''
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
        return Response({'message': str(
            zone_add_rr.add_resource_record(request))})

    def post(self, request, pk):
        zone_obj = self.get_object(pk)
        zone_del_rr = ZoneOperations(zone_obj.path_file, zone_obj.zone_name)
        return Response({'message': str(
            zone_del_rr.del_resource_record(request))})


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
