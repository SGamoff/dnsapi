from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, \
        RetrieveAPIView, DestroyAPIView
from apps.editor.models import Service, Zone, RR
from apps.editor.serializers import ServiceSerilializers, ZoneSerilializers, RRSerilializers


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

