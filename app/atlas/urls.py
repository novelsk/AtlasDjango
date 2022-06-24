from django.urls import path, re_path
from . import views

app_name = 'atlas'

urlpatterns = [
    # path('api/ai/<int:pk>', views.api_ai_change_sts)
    path('api/chart', views.api_chart),
    path('rabbit_data', views.sensors_data),
    path('accounts/login/', views.AtlasLoginView.as_view(), name='login'),
    path('accounts/login', views.AtlasLoginView.as_view(), name='login'),
    path('accounts/logout', views.AtlasLogoutView.as_view(), name='logout'),
    path('accounts/user', views.account, name='account'),
    path('main', views.base2, name='new_main'),
    path('analytics', views.analytics, name='analytics'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('archive', views.archive, name='archive'),
    path('', views.index, name='index'),
]
