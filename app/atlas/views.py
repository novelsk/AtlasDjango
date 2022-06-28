# from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from django.http import JsonResponse, QueryDict
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from .forms import LoginForm, UserForm, MLForm
from .models import SensorData, SensorError, Sensor, Object, UserAccessGroups, Company, SensorMLSettings, ObjectEvent


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
def company_objects(request, pk):
    context = {}
    company = Company.objects.get(pk=pk)
    context['company'] = company
    objects = Object.objects.filter(id_company=company)
    context['object_list'] = list(objects)
    return render(request, 'company.html', context)


@login_required
def object_sensors(request, pk):
    context = {}
    object_item = Object.objects.get(pk=pk)
    context['object'] = object_item
    sensors = Sensor.objects.filter(id_object=object_item).order_by('id_sensor_repr')
    context['sensors_list'] = list(sensors)
    return render(request, 'object.html', context)


@login_required
def sensor_chart(request, object_id, sensor_id):
    context = {}
    object_item = Object.objects.get(pk=object_id)
    context['object'] = object_item
    sensor = Sensor.objects.get(pk=sensor_id)
    context['sensor'] = sensor
    return render(request, 'chart.html', context)


@login_required
def object_events(request, id_sensor):
    context = {}
    object_item = Object.objects.get(pk=id_sensor)
    context['object'] = object_item
    events = ObjectEvent.objects.filter(id_object=object_item).order_by('status')
    context['events_list'] = list(events)
    return render(request, 'event.html', context)


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


@login_required
def settings_ml(request, id_sensor):
    context = {}
    sensor = Sensor.objects.get(pk=id_sensor)
    context['sensor'] = sensor
    if not user_access_sensor(request, id_sensor):
        return redirect('atlas:sensor', sensor.id_object.id, sensor.id)

    # ошибка бесконечного создания настроек
    try:
        settings = SensorMLSettings.objects.get(id_sensor=sensor)
    except ObjectDoesNotExist:
        settings = SensorMLSettings.objects.create(id_sensor=sensor).save()
    if request.method == 'POST':
        form = MLForm(request.POST, instance=settings)
        context['form'] = form
        if form.is_valid():
            form.save()
            form.clean()
            context['success'] = True
        return render(request, 'mlsettings.html', context)
    else:
        form = MLForm(instance=settings)
        context['form'] = form
        return render(request, 'mlsettings.html', context)


class AtlasLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm


class AtlasLogoutView(LogoutView):
    template_name = 'logout.html'
    next_page = 'atlas:index'


# api
@api_view(['POST'])
def sensors_data(request):
    """
    Функция только для создания модели данных Django
    """
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
def api_chart(request, object_id, sensor_id=None):
    if request.method == 'GET':
        if sensor_id is None:
            pass
        else:
            sensor = Sensor.objects.get(id_object__pk=object_id, pk=sensor_id)
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


def user_access_company(request, company):
    """
    Возврщает QuerySet групп, доступных пользвоателю, по компании
    """
    groups = UserAccessGroups.objects.filter(users=request.user, companys=company)
    if groups.count() != 0:
        return groups
    else:
        return None


def user_access_sensor(request, sensor_id):
    """
    Проверяет наличие доступа к изменению датчика
    """
    company = Sensor.objects.get(pk=sensor_id).id_object.id_company
    groups = user_access_company(request, company)
    if groups is not None:
        for i in groups:
            i = i  # type: UserAccessGroups
            if i.write:
                return True
    return False


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
