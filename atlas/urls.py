from django.urls import path, re_path
from . import views

app_name = 'atlas'

urlpatterns = [
    path('test', views.test),
    path('api/cmn/<int:group>', views.api_cmn),
    re_path(r'api/cmn/*', views.api_cmn),
    path('accounts/login', views.AtlasLoginView.as_view(), name='login'),
    path('accounts/logout', views.AtlasLogoutView.as_view(), name='logout'),
    path('table', views.table, name='table'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('', views.index, name='index'),
]
