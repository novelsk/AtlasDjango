from django.urls import path
from . import views

app_name = 'atlas'

urlpatterns = [
    path('accounts/login', views.AtlasLoginView.as_view(), name='login'),
    path('accounts/logout', views.AtlasLogoutView.as_view(), name='logout'),
    path('graph', views.graph, name='graph'),
    path('', views.index, name='index'),
]
