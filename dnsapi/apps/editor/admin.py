from django.contrib import admin

# Register your models here.

from apps.editor.models import Zone, Service, RR


@admin.register(RR)
class RRAdmin(admin.ModelAdmin):
    list_display = ('recordName', 'textData')

    class Meta:
        model = RR


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('zone_name', 'path_file', 'zone_type', 'service')

    class Meta:
        model = Zone


@admin.register(Service)
class ServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'port')

    class Meta:
        model = Service