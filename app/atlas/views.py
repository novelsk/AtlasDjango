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
def base2(request):
    company_query = user_company_query(request)
    objects = Object.objects.none()
    for i in company_query:
        i = i  # type: Company
        objects = objects.union(i.object_company.all())
    objects = list(objects)
    context = {'object_list': objects}
    return render(request, 'base2.html', context)


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
            context['success'].append(True)
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
        current_object = Object.objects.get(pk=data.get('id_object'))
        context = {'': 'csrf checked'}
        if current_object is not None:
            current_sensor = Sensor.objects.get(id_object=current_object, id_sensor_repr=data.get('id_sensor'))
            context = {'': 'current_object is not None'}
            if current_sensor is not None:
                context = {'': 'if current_sensor is not None'}
                sensor_data = SensorData.objects.create(
                    id_sensor=current_sensor, date=data.get('date'), mode=data.get('mode'),
                    ai_max=data.get('ai_max'), ai_min=data.get('ai_min'),
                    ai_mean=data.get('ai_mean'), stat_min=data.get('stat_min'),
                    stat_max=data.get('stat_max'), ml_min=data.get('ml_min'),
                    ml_max=data.get('ml_max'), status=data.get('status'),
                )
                previous_data = SensorData.objects.all().last()
                error = int(data.get('error'))

                '''
                Если есть ошибка то
                    Если у прошлых данных нет ошибки, то
                        Создается новый журнал ошибок, сохраняется
                        Новые данные записываются в журнал
                    Иначе если предыдущая ошибка равна текущей, то
                        текущая ошибка записывается в существующий журнал
                    Иначе
                        Предыдущий журнал закрывается, время заверешния из предыдущей ошибки
                        Создается новый журнал ошибок, сохраняется
                        Новые данные записываются в журнал
                '''

                if error == 0:
                    if previous_data.id_error_log is not None:
                        previous_data.id_error_log.error_end_date = previous_data.date
                else:
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
                sensor_data.save()
                context[''] = 'GOOD'
    return JsonResponse(context, safe=False)


@api_view(['GET'])
def api_chart(request):
    if request.method == 'GET':
        sensor = Sensor.objects.first()
        count = int(request.GET.get('count'))
        data_query = sensor.data_sensor.order_by('-date')[:count]  # type: QuerySet
        context = {
            'ai_max': [], 'ai_min': [],
            'ai_mean': [], 'stat_min': [], 'stat_max': [],
            'ml_min': [], 'ml_max': [], 'status': [], 'date': []}
        for data in data_query:
            context['ai_max'].append(data.ai_max)
            context['ai_min'].append(data.ai_min)
            context['ai_mean'].append(data.ai_mean)
            context['stat_min'].append(data.stat_min)
            context['stat_max'].append(data.stat_max)
            context['ml_min'].append(data.ml_min)
            context['ml_max'].append(data.ml_max)
            context['status'].append(data.status)
            context['date'].append(data.date.time())
        return JsonResponse(context, safe=False)


# logic
def user_company_query(request):
    """Возврщает QuerySet, компаний которые доступны пользователю"""
    current_user = AtlasUser.objects.get(pk=request.user.pk)
    user_groups = current_user.useraccessgroups_set.all()
    company_query = Company.objects.none()  # type: QuerySet
    for i in user_groups:
        company_query = company_query.union(i.companys.all())
    return company_query

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
