from django.urls import path
from . import views

app_name = 'atlas'

urlpatterns = [
    path('company/<int:pk>', views.company_objects, name='company'),
    path('events/edit/<int:event_id>', views.event_edit, name='event_edit'),
    path('sensor/archive/<int:sensor_id>', views.archive, name='archive'),
    path('object/archive/<int:object_id>', views.archive_object, name='archive_object'),
    path('object/<int:object_id>/events/new', views.event_new, name='event_new'),
    path('object/<int:object_id>/events', views.object_events, name='events'),
    path('object/<int:sensor_id>/settings', views.settings_sensor, name='settings_sensor'),
    path('object/<int:object_id>/<int:sensor_id>', views.sensor_chart, name='sensor'),
    path('object/<int:pk>', views.object_sensors, name='object'),
    path('api/confirm_error', views.api_confirm_error),
    path('api/chart/object/<int:object_id>/<int:sensor_id>', views.api_chart),
    path('api/chart/object/<int:object_id>', views.api_object_chart),
    path('rabbit_data', views.sensors_data),
    path('accounts/login/', views.AtlasLoginView.as_view(), name='login'),
    path('accounts/login', views.AtlasLoginView.as_view(), name='login'),
    path('accounts/logout', views.AtlasLogoutView.as_view(), name='logout'),
    path('accounts/create', views.create_user, name='create_user'),
    path('accounts/user', views.account, name='account'),
    path('', views.index, name='index'),
]
