from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import LoginForm
from .models import Cmn, Ai, AtlasUser
from .serializers import CmnSerializer


def index(request):
    return render(request, 'index.html')


def test(request):
    current_user = AtlasUser.objects.filter(pk=request.user.pk)[0]
    context = {'user_groups': current_user.objects_ai_groups}
    obj = Cmn.objects.filter(access_group=current_user.objects_ai_groups[0])  # настроить возможность выбора группы
    return render(request, 'test.html', context=context)


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def table(request):
    return render(request, 'table.html')


class AtlasLoginView(LoginView):
    template_name = 'auth-signin.html'
    authentication_form = LoginForm


class AtlasLogoutView(LogoutView):
    template_name = 'logout.html'
    next_page = 'atlas:index'


# api
@login_required
@api_view(['GET'])
def api_cmn(request, count=None):
    if request.method == 'GET':
        current_user = AtlasUser.objects.get(pk=request.user.pk)
        if count is None:
            cmn_objects = Cmn.objects.filter(access_group=current_user.objects_ai_groups[0])[:60]  # настроить выбор группы
        else:
            cmn_objects = Cmn.objects.filter(access_group=current_user.objects_ai_groups[0])[:count]

        ai_out = [[], [], [], [], [], [], [], [], [], []]
        for item in cmn_objects:
            ai_out[0].append(item.ai1)
            ai_out[1].append(item.ai2)
            ai_out[2].append(item.ai3)
            ai_out[3].append(item.ai4)
            ai_out[4].append(item.ai5)
            ai_out[5].append(item.ai6)
            ai_out[6].append(item.ai7)
            ai_out[7].append(item.ai8)
            ai_out[8].append(item.ai9)
            ai_out[9].append(item.ai10)
        return JsonResponse({'cmn_ais': ai_out}, safe=False)
