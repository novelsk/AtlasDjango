# from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import LoginForm, UserForm


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def analytics(request):
    return render(request, 'analytics.html')


@login_required
def archive(request):
    return render(request, 'archive.html')


@login_required
def account(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        context = {'form': form}
        if form.is_valid():
            form.save()
            form.clean()
            context['success'] = True
        return render(request, 'account.html', context)
    else:
        form = UserForm(instance=request.user)
        context = {'form': form}
        return render(request, 'account.html', context)


class AtlasLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm


class AtlasLogoutView(LogoutView):
    template_name = 'logout.html'
    next_page = 'atlas:index'


# # api
# @api_view(['GET'])
# def api_cmn_board(request, count=None):
#     if request.method == 'GET':
#         current_user = AtlasUser.objects.get(pk=request.user.pk)
#         user_group = get_user_cmngroup(request, current_user)
#         # cmn_objects = Cmn.objects.order_by('-pk').filter(access_group=user_group)
#
#         out = ()
#         return JsonResponse({'cmn_ais': out}, safe=False)


# @api_view(['GET'])
# def api_ai_change_sts(request, pk=None):
#     if request.method == 'GET':
#         current_user = AtlasUser.objects.get(pk=request.user.pk)
#         if pk is not None:
#             temp = Ai.objects.get(pk=pk)
#             if temp.access_group in current_user.objects_ai_groups:
#                 temp.sts = 2
#                 temp.save()
#                 return JsonResponse({'': 'success'}, safe=False)
#             else:
#                 return JsonResponse({'': 'failed'}, safe=False)
#         else:
#             return JsonResponse({'': 'failed'}, safe=False)


# @api_view(['GET'])
# def api_archive(request):
#     if request.method == 'GET':
#         current_user = AtlasUser.objects.get(pk=request.user.pk)
#         table_objects = Ai.objects.filter(err__gt=0)
#         temp = []
#         for item in table_objects:
#             if item.access_group in current_user.objects_ai_groups:
#                 temp.append(item)
#         serializer = AiSerializer(temp, many=True)
#         return Response(serializer.data)


# def get_user_aigroup(request, user):
#     group_num = request.GET.get('num')
#     user_group = user.objects_ai_groups[0]
#     if group_num is not None:
#         try:
#             if int(group_num) in user.objects_ai_groups:
#                 user_group = group_num
#         except ValueError:
#             pass
#     return user_group
