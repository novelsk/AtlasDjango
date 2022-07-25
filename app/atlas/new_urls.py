from django.urls import path
from . import new_views

app_name = 'new'

urlpatterns = [
    path('', new_views.index, name='index'),
    path('sensor/trend', new_views.sensor_trend, name='sensor_trend'),
    path('sensor/errors', new_views.sensor_errors, name='sensor_errors'),
    path('sensor/settings', new_views.sensor_settings, name='sensor_settings'),
    path('object/trend', new_views.object_trend, name='trend'),
    path('object/analytics', new_views.object_analytics, name='analytics'),
    path('object/scheme', new_views.object_scheme, name='scheme'),
    path('object/archive', new_views.object_archive, name='archive'),
    path('object/events', new_views.object_events, name='object_events'),
    path('object/settings', new_views.object_settings, name='object_settings'),
    path('api/sensor/chart', new_views.api_sensor_chart),
    path('api/sensor/confirm_errors_all', new_views.api_sensor_confirm_errors_all),
    path('api/object/chart', new_views.api_object_chart),
]
