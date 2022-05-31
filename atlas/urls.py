from django.urls import path, re_path
from . import views

app_name = 'atlas'

urlpatterns = [
    path('api/ai', views.api_ai),
    path('api/ai/<int:pk>', views.api_ai_change_sts),
    path('api/cmn/<int:count>', views.api_cmn),
    path('api/cmn', views.api_cmn),
    path('accounts/login', views.AtlasLoginView.as_view(), name='login'),
    path('accounts/logout', views.AtlasLogoutView.as_view(), name='logout'),
    path('table', views.table, name='table'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('', views.index, name='index'),
]
