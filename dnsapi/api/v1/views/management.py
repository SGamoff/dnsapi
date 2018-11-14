import coreapi
import coreschema
from api.v1.serializers import ServiceSerilializers, ZoneSerilializers
from apps.editor.utils.zoneoperations import ZoneOperations, \
    ResourceRecordOperations
from apps.editor.utils.serviceoperations import ServiceOpertaions
from apps.editor.models import Service, Zone
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from rest_framework import permissions
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
        return Response({'message': str(zone_import.read_zone_from_txt())})


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
        return Response({'message': str(zone_export.export_zone_to_txt())})


class ZoneResourceRecordViewSchema(AutoSchema):

    def get_manual_fields(self, path, method):
        extra_fields = []
        if method == "GET":
            pass
        if method == "DELETE":
            extra_fields = [
                coreapi.Field(
                    "rr_name", required=False,
                    location="form", schema=coreschema.String(
                        description="Resource record Name(default @)"
                    )
                ),
                coreapi.Field(
                    "rr_type", required=True,
                    location="form", schema=coreschema.String(
                        description="Resource record Type"
                    )
                )
            ]
        if method == "POST":
            extra_fields = [
                coreapi.Field(
                    "rr_name", required=False,
                    location="form", schema=coreschema.String(
                        description="Resource record Name(default @)"
                    )
                ),
                coreapi.Field(
                    "rr_type", required=True,
                    location="form", schema=coreschema.String(
                        description="Resource record Type"
                    )
                ),
                coreapi.Field(
                    "rr_ttl", required=False,
                    location="form", schema=coreschema.Integer(
                        description="Resource record TTL(default from SOA)",
                        maximum=2147483647, minimum=300
                    )
                ),
                coreapi.Field(
                    "rr_class", required=False,
                    location="form", schema=coreschema.String(
                        description="Resource record Class(default IN)",
                        max_length=3
                    )
                ),
                coreapi.Field(
                    "rr_text", required=True,
                    location="form", schema=coreschema.String(
                        description="Resource record Content"
                    )
                ),
            ]

        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields


class ZoneResourceRecord(APIView):
    """
    A router for API Zone resource records operations by zone ID POST
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    schema = ZoneResourceRecordViewSchema()

    @staticmethod
    def get_object(pk):
        try:
            return Zone.objects.get(zone_id=pk)
        except Zone.DoesNotExist:
            raise Http404

    def get_zone(self, pk):
        zone_obj = self.get_object(pk)
        zone_rr = ZoneOperations(zone_obj.path_file, zone_obj.zone_name)
        return zone_rr

    def get(self, request, pk):
        rr_text = self.get_object(pk)
        find_record = ResourceRecordOperations(rr_text.zone_id)
        return Response(str(find_record.find_and_return_records()))

    def post(self, request, pk):
        return Response({'message': str(
            self.get_zone(pk).add_resource_record(request))})

    def delete(self, request, pk):
        return Response({'message': str(
            self.get_zone(pk).del_resource_record(request))})


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


class ZoneReload(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def get_service_obj(pk):
        try:
            zone_obj=Zone.objects.get(zone_id__exact=pk)
            serv_obj =Service.objects.get(name__exact=zone_obj.service.name)
            return ServiceOpertaions(serv_obj.name, serv_obj.port, zone_obj.zone_name)
        except Service.DoesNotExist:
            raise Http404

    def post(self, request, pk):
        return Response({"message": str(
            self.get_service_obj(pk).rndc_reload_service())})

