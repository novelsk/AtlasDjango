from django.urls import path, include
from . import views

app_name = 'atlas'

urlpatterns = [
    path('test', views.test, name='test'),
    path('new/', include('atlas.new_urls'), name='new'),
    path('api/confirm_error', views.api_confirm_error),
    path('api/setter', views.api_object_setter),
    path('rabbit/data', views.sensors_data),
    path('accounts/login/', views.AtlasLoginView.as_view(), name='login'),
    path('accounts/login', views.AtlasLoginView.as_view(), name='login'),
    path('accounts/logout', views.AtlasLogoutView.as_view(), name='logout'),
    path('', views.index, name='index'),
]
