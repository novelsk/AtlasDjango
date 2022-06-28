from django.urls import path, re_path
from . import views

app_name = 'atlas'

urlpatterns = [
    path('company/<int:pk>', views.company_objects, name='company'),
    path('object/<int:id_sensor>/events', views.object_events, name='events'),
    path('object/<int:id_sensor>/settings/ml', views.settings_ml, name='settings_ml'),
    path('object/<int:object_id>/<int:sensor_id>', views.sensor_chart, name='sensor'),
    path('object/<int:pk>', views.object_sensors, name='object'),
    path('api/chart/object/<int:object_id>/<int:sensor_id>', views.api_chart),
    path('rabbit_data', views.sensors_data),
    # old paths
    path('accounts/login/', views.AtlasLoginView.as_view(), name='login'),
    path('accounts/login', views.AtlasLoginView.as_view(), name='login'),
    path('accounts/logout', views.AtlasLogoutView.as_view(), name='logout'),
    path('accounts/user', views.account, name='account'),
    path('analytics', views.analytics, name='analytics'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('archive', views.archive, name='archive'),
    path('', views.index, name='index'),
]
