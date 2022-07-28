from django.urls import path
from . import new_views

app_name = 'new'

urlpatterns = [
    path('sensor/trend', new_views.sensor_trend, name='sensor_trend'),
    path('sensor/errors', new_views.sensor_errors, name='sensor_errors'),
    path('sensor/settings', new_views.sensor_settings, name='sensor_settings'),
    path('object/trend', new_views.object_trend, name='object_trend'),
    path('object/analytics', new_views.object_analytics, name='object_analytics'),
    path('object/sensors', new_views.object_sensors, name='object_sensors'),
    path('object/scheme', new_views.object_scheme, name='object_scheme'),
    path('object/archive', new_views.object_archive, name='object_archive'),
    path('object/events/edit', new_views.object_event_edit, name='object_event_edit'),
    path('object/events/new', new_views.object_events_new, name='object_events_new'),
    path('object/events', new_views.object_events, name='object_events'),
    path('object/settings', new_views.object_settings, name='object_settings'),
    path('сompany', new_views.company, name='company'),
    path('accounts/create', new_views.create_user, name='create_user'),
    path('accounts/user', new_views.account, name='account'),
    path('', new_views.index, name='index'),
    path('api/sensor/chart', new_views.api_sensor_chart),
    path('api/sensor/confirm_errors_all', new_views.api_sensor_confirm_errors_all),
    path('api/object/chart', new_views.api_object_chart),
]
