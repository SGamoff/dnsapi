import requests

from django.test import TestCase
from os import path
from pathlib import Path

from api.v1.views.management import ZoneOperations
from apps.editor.models import Service, Zone
from apps.editor.emums import ZoneTypes, ServerTypes

TEST_ZONE_FILE = path.join(path.dirname(__file__), 'testdata.zone')
TEST_ZONE_EXPORT_FILE = path.join(path.dirname(__file__), 'testexportdata.zone')

class ZoneOperationsTest(TestCase):

    def setUp(self):
        Service.objects.create(name='1.1.1.1', port='53', server_type=ServerTypes.BIND9)
        Zone.objects.create(path_file=TEST_ZONE_FILE, zone_name='testzone', zone_type=ZoneTypes.FWD,
                            service=Service.objects.get(id=1))

    def test_import_zone_from_file(self):
        """
        Test equals zone.zone_text and file content
        :return:
        """
        obj = Zone.objects.get(zone_name__exact='testzone')
        obj_import = ZoneOperations(obj.path_file, obj.zone_name)
        obj_import.read_zone_from_txt()
        obj2 = Zone.objects.get(zone_name__exact='testzone')
        f = open(TEST_ZONE_FILE)
        self.assertEqual(f.read(), obj2.zone_text)

    def test_export_zone_to_file(self):
        """
        Test equals export file and database text file
        :return:
        """
        obj = Zone.objects.get(zone_name__exact='testzone')
        obj_ops = ZoneOperations(obj.path_file, obj.zone_name)
        obj_ops.read_zone_from_txt()
        Path(TEST_ZONE_EXPORT_FILE).touch()
        obj_export_ops = ZoneOperations(TEST_ZONE_EXPORT_FILE, 'testzone')
        obj_export_ops.export_zone_to_txt()
        file_import = open(TEST_ZONE_FILE)
        file_export = open(TEST_ZONE_EXPORT_FILE)
        self.assertEqual(file_export.read(), file_import.read())

    def test_add_record(self):
        obj = Zone.objects.get(zone_name__exact='testzone')
        obj_ops = ZoneOperations(obj.path_file, obj.zone_name)
        obj_ops.read_zone_from_txt()
        payload = {
            'rrtype': 'TXT',
            'rrname': 'testrecord',
            'rrtext': 'text record'
        }
        r = requests.post('/',data=payload)
        Path(TEST_ZONE_EXPORT_FILE).touch()
        obj_export_ops = ZoneOperations(TEST_ZONE_EXPORT_FILE, 'testzone')
        obj_export_ops.add_resource_record(r)
        obj_export_ops.export_zone_to_txt()
        self.assertEqual('test', obj_ops.zone_text)

    @classmethod
    def tearDownClass(cls):
        Path(TEST_ZONE_EXPORT_FILE).unlink()