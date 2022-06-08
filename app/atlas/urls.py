from django.urls import path, re_path
from . import views

app_name = 'atlas'

urlpatterns = [
    path('api/user/groups', views.api_user_groups),
    path('api/archive', views.api_archive),
    path('api/ai', views.api_ai),
    path('api/ai/<int:pk>', views.api_ai_change_sts),
    path('api/ai_board/<int:count>', views.api_ai_board),
    path('api/ai_board', views.api_ai_board),
    path('api/cmn/<int:count>', views.api_cmn_board),
    path('api/cmn', views.api_cmn_board),
    path('accounts/login', views.AtlasLoginView.as_view(), name='login'),
    path('accounts/logout', views.AtlasLogoutView.as_view(), name='logout'),
    path('table', views.table, name='table'),
    path('analytics', views.analytics, name='analytics'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('archive', views.archive, name='archive'),
    path('', views.index, name='index'),
]
