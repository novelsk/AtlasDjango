# from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import QuerySet
from django.http import JsonResponse, QueryDict
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import LoginForm, UserForm
from .models import SensorData, SensorError, Sensor, Object, AtlasUser, UserAccessGroups, Company


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


# api
@api_view(['POST'])
def sensors_data(request):
    data = request.POST  # type: QueryDict
    context = {'': 'BAD'}
    if data.get('csrf') == 'a very secret key':
        context[''] = 'csrf verification passed'
        current_object = Object.objects.get(pk=data.get('id_object'))
        if current_object is not None:
            context[''] = 'object founded'
            current_sensor = Sensor.objects.get(id_object=current_object, id_sensor_repr=data.get('id_sensor'))
            if current_sensor is not None:
                context[''] = 'sensor founded'
                sensor_data = SensorData.objects.create(
                    id_sensor=current_sensor, date=data.get('date'), mode=data.get('mode'),
                    ai_max=data.get('ai_max'), ai_min=data.get('ai_min'),
                    ai_mean=data.get('ai_mean'), stat_min=data.get('stat_min'),
                    stat_max=data.get('stat_max'), ml_min=data.get('ml_min'),
                    ml_max=data.get('ml_max'), status=data.get('status'),
                )
                previous_data = SensorData.objects.all().last()
                error = data.get('error')

                '''
                Если есть ошибка то
                    Если у прошлых данных нет ошибки, то
                        Создается новый журнал ошибок, сохраняется
                        Новые данные записываются в журнал
                    Иначе если у 
                '''

                if error != 0:
                    if previous_data.id_error_log is None:
                        new_journal = SensorError.objects.create(
                            id_sensor=current_sensor, error=error, error_start_date=sensor_data.date)
                        new_journal.save()
                        sensor_data.id_error_log = new_journal
                    elif previous_data.id_error_log.error == error:
                        sensor_data.id_error_log = previous_data.id_error_log
                    else:
                        previous_data.id_error_log.error_end_date = previous_data.date
                        new_journal = SensorError.objects.create(
                            id_sensor=current_sensor, error=error, error_start_date=sensor_data.date)
                        new_journal.save()
                        sensor_data.id_error_log = new_journal
                else:
                    if previous_data.id_error_log is not None:
                        previous_data.id_error_log.error_end_date = previous_data.date

                sensor_data.save()
                context[''] = 'GOOD'
    return JsonResponse(context, safe=False)


@api_view(['GET'])
def api_chart(request):
    if request.method == 'GET':
        current_user = AtlasUser.objects.get(pk=request.user.pk)
        user_groups = current_user.useraccessgroups_set.all()
        companys = Company.objects.none()  # type: QuerySet
        test = {}
        for i in user_groups:
            test[i.pk] = i.name
            companys.union(companys, i.companys)  # type: QuerySet
        # for company in user_companys:
        #     out[company.pk] = company.name
        return JsonResponse({'': test}, safe=False)


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
