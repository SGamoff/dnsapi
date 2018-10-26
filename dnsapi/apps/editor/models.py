from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
# from django.urls import reverse


from apps.editor.emums import RecordClassTypes, \
     RecordResourceTypes, ZoneTypes, ServerTypes

# Create your models here.


class Service(models.Model):
    name = models.CharField(default='127.0.0.1', null=False, max_length=255, verbose_name='DNS/IP Server')
    port = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(65535), ],
                                       verbose_name='Port')
    server_type = models.CharField(default=ServerTypes.BIND9,
        editable=False, choices=ServerTypes.Choices, max_length=8, verbose_name='Type server')

    def __str__(self):
        return self.name


class Zone(models.Model):
    path_file = models.CharField(max_length=4096, verbose_name='Zone file path')
    zone_name = models.CharField(default='None', primary_key=True, max_length=255)
    zone_type = models.CharField(default=ZoneTypes.FWD,
        choices = ZoneTypes.Choices, max_length=8, verbose_name='Type zone')
    service = models.ForeignKey(Service, on_delete=models.CASCADE,
        null=False, blank=False, verbose_name='Server')

    def __str__(self):
        return self.zone_name


class RR(models.Model):
    recordName = models.CharField(default='', max_length=255, verbose_name='Record Name')
    textData = models.TextField(default='', verbose_name='Record Data')
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, null=False, blank=False, verbose_name='Zone')

    def __str__(self):
        return self.recorddata



