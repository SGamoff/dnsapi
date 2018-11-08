import ipaddress
from django.test import TestCase
from django.core.exceptions import ValidationError

from apps.editor.models import Zone, Service
from apps.editor.emums import ServerTypes, ZoneTypes

class ServiceModelTest(TestCase):

    @classmethod
    def setUp(self):
        Service.objects.create(name='1.1.1.1', port='53', server_type=ServerTypes.BIND9)

    def test_name(self):
        serv = Service.objects.get(id=1)
        field_name = serv._meta.get_field('name').verbose_name
        self.assertEqual(field_name, 'DNS/IP Server')

    def test_port_max_value(self):
        serv = Service(name='test.org', port='65536', server_type=ServerTypes.BIND9)
        with self.assertRaises(ValidationError):
            if serv.full_clean():
                serv.save()
        self.assertEqual(Service.objects.filter(port='65536').count(), 0)

    def test_port_min_value(self):
        serv = Service(name='test.org', port='0', server_type=ServerTypes.BIND9)
        with self.assertRaises(ValidationError):
            if serv.full_clean():
                serv.save()
        self.assertEqual(Service.objects.filter(port='0').count(), 0)

    def test_service_type_enums(self):
        self.assertEqual(ServerTypes.BIND9, 'bind9')



class ZoneModelTest(TestCase):

    @classmethod
    def setUp(self):
        Service.objects.create(name='1.1.1.1', port='53', server_type=ServerTypes.BIND9)
        Zone.objects.create(path_file='/var/lib/bind/localhost.db', zone_name='localhost', zone_type=ZoneTypes.FWD,
            service=Service.objects.get(id=1))

    def test_name(self):
        zon = Zone.objects.get(zone_id=1)
        field_name = zon._meta.get_field('path_file').verbose_name
        self.assertEqual(field_name, 'Zone file path')