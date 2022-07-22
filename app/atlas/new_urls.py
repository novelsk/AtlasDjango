from django.urls import path
from . import new_views

app_name = 'new'

urlpatterns = [
    path('', new_views.index, name='index'),
    path('/object/trend', new_views.trend, name='trend'),
    path('/object/analytics', new_views.analytics, name='analytics'),
    path('/object/scheme', new_views.scheme, name='scheme'),
    path('/object/archive', new_views.archive, name='archive'),
    path('/object/events', new_views.object_events, name='object_events'),
    path('/object/settings', new_views.object_settings, name='object_settings'),
    path('/api/object/chart', new_views.api_object_chart),
]
