from django.contrib import admin
from .models import Company, Object, Sensor, SensorData, SensorMLSettings, ObjectEvent, SensorError, \
    AtlasUser, UserAccessGroups


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'info')
    list_display_links = ('name', )


class ObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'info', 'id_company')
    list_display_links = ('name', )


class SensorAdmin(admin.ModelAdmin):
    list_display = ('name', 'info', 'id_object')
    list_display_links = ('name', )


class SensorDataAdmin(admin.ModelAdmin):
    list_display = ('id_sensor', 'date', 'mode', 'status')
    list_display_links = ('id_sensor', )


class SensorErrorAdmin(admin.ModelAdmin):
    list_display = ('id_sensor', 'error', 'error_start_date')
    list_display_links = ('id_sensor',)


class SensorMLSettingsAdmin(admin.ModelAdmin):
    list_display = ('id_sensor', 'info')
    list_display_links = ('id_sensor', )


class ObjectEventAdmin(admin.ModelAdmin):
    list_display = ('id_object', 'status', 'date_of_creation', 'date_of_service_planned')
    list_display_links = ('id_object', 'status')


class AtlasUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')
    list_display_links = ('username', )


class UserAccessGroupsAdmin(admin.ModelAdmin):
    list_display = ('name', 'info', 'read', 'write')
    list_display_links = ('name', )


admin.site.register(Company, CompanyAdmin)
admin.site.register(Object, ObjectAdmin)
admin.site.register(ObjectEvent, ObjectEventAdmin)
admin.site.register(Sensor, SensorAdmin)
admin.site.register(SensorData, SensorDataAdmin)
admin.site.register(SensorMLSettings, SensorMLSettingsAdmin)
admin.site.register(SensorError, SensorErrorAdmin)
admin.site.register(AtlasUser, AtlasUserAdmin)
admin.site.register(UserAccessGroups, UserAccessGroupsAdmin)
