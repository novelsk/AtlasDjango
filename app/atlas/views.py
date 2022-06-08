from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import LoginForm
from .models import Cmn, Ai, AtlasUser
from .serializers import AiSerializer, UserGroups


def index(request):
    return render(request, 'index.html')


@login_required
@never_cache
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
@never_cache
def analytics(request):
    return render(request, 'analytics.html')


@login_required
@never_cache
def table(request):
    return render(request, 'table.html')


@login_required
@never_cache
def archive(request):
    return render(request, 'archive.html')


class AtlasLoginView(LoginView):
    template_name = 'auth-signin.html'
    authentication_form = LoginForm


class AtlasLogoutView(LogoutView):
    template_name = 'logout.html'
    next_page = 'atlas:index'


# api
@api_view(['GET'])
def api_cmn_board(request, count=None):
    if request.method == 'GET':
        current_user = AtlasUser.objects.get(pk=request.user.pk)
        user_group = get_user_cmngroup(request, current_user)
        cmn_objects = Cmn.objects.order_by('-pk').filter(access_group=user_group)

        if count is None:
            cmn_objects = cmn_objects[:60]
        else:
            cmn_objects = cmn_objects[:count]

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


@api_view(['GET'])
def api_ai_board(request, count=None):
    if request.method == 'GET':
        current_user = AtlasUser.objects.get(pk=request.user.pk)
        user_group = get_user_aigroup(request, current_user)
        ai_objects = Ai.objects.order_by('-pk').filter(access_group=user_group)
        if count is None:
            ai_objects = ai_objects[:60]
        else:
            ai_objects = ai_objects[:count]

        ai_out = {'datain': [], 'mode': [], 'aimean': [], 'statmin': [],
                  'statmax': [], 'mlmin': [], 'mlmax': [], 'err': []}
        for item in ai_objects:
            ai_out['datain'].append(item.datain)
            ai_out['mode'].append(item.mode)
            ai_out['aimean'].append(item.aimean)
            ai_out['statmin'].append(item.statmin)
            ai_out['statmax'].append(item.statmax)
            ai_out['mlmin'].append(item.mlmin)
            ai_out['mlmax'].append(item.mlmax)
            ai_out['err'].append(item.err)
        return JsonResponse(ai_out, safe=False)


@api_view(['GET'])
def api_ai(request):
    if request.method == 'GET':
        current_user = AtlasUser.objects.get(pk=request.user.pk)
        user_group = get_user_aigroup(request, current_user)

        table_objects = Ai.objects.filter(access_group=user_group, sts=1, err__gt=0).reverse()[:20]
        serializer = AiSerializer(table_objects, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def api_ai_change_sts(request, pk=None):
    if request.method == 'GET':
        current_user = AtlasUser.objects.get(pk=request.user.pk)
        if pk is not None:
            temp = Ai.objects.get(pk=pk)
            if temp.access_group in current_user.objects_ai_groups:
                temp.sts = 2
                temp.save()
                return JsonResponse({'': 'success'}, safe=False)
            else:
                return JsonResponse({'': 'failed'}, safe=False)
        else:
            return JsonResponse({'': 'failed'}, safe=False)


@api_view(['GET'])
def api_archive(request):
    if request.method == 'GET':
        current_user = AtlasUser.objects.get(pk=request.user.pk)
        table_objects = Ai.objects.filter(err__gt=0)
        temp = []
        for item in table_objects:
            if item.access_group in current_user.objects_ai_groups:
                temp.append(item)
        serializer = AiSerializer(temp, many=True)
        return Response(serializer.data)


def get_user_aigroup(request, user):
    group_num = request.GET.get('num')
    user_group = user.objects_ai_groups[0]
    if group_num is not None:
        try:
            if int(group_num) in user.objects_ai_groups:
                user_group = group_num
        except ValueError:
            pass
    return user_group


def get_user_cmngroup(request, user):
    group_num = request.GET.get('num')
    user_group = user.objects_cmn_groups[0]
    if group_num is not None:
        try:
            if int(group_num) in user.objects_cmn_groups:
                user_group = group_num
        except ValueError:
            pass
    return user_group


@api_view(['GET'])
def api_user_groups(request):
    serializer = UserGroups(AtlasUser.objects.get(pk=request.user.pk), many=False)
    return Response(serializer.data)
