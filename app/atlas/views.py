from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse, QueryDict
from django.shortcuts import render, redirect
from django.utils import timezone
from rest_framework.decorators import api_view
from .forms import LoginForm
from .models import SensorData, SensorError, Sensor
from .logical import user_access_sensor_read
from .util import int_round
from .mail import on_error


@login_required
def test(request):
    temp = SensorError.objects.last()  # type: SensorError
    data = temp.data_error.count()
    context = {'': data}
    return JsonResponse(context, safe=False)


@login_required
def index(request):
    return redirect('atlas:new:index')


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
        context = {'': 'csrf checked'}
        current_sensor = Sensor.objects.get(id_object__id_object_repr=data.get('id_object'),
                                            id_sensor_repr=data.get('id_sensor'))
        if current_sensor is not None:
            context = {'': 'if current_sensor is not None'}
            previous_data = SensorData.objects.filter(id_sensor=current_sensor).last()  # type: SensorData
            sensor_data = SensorData.objects.create(
                id_sensor=current_sensor, date=data.get('date'), mode=int_round(data.get('mode')),
                ai_max=data.get('ai_max'), ai_min=data.get('ai_min'),
                ai_mean=data.get('ai_mean'), stat_min=data.get('stat_min'),
                stat_max=data.get('stat_max'), ml_min=data.get('ml_min'),
                ml_max=data.get('ml_max'), status=data.get('status'),
            )
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
                    previous_data.id_error_log.save()
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
            if error:
                on_error(sensor_data)
    return JsonResponse(context, safe=False)


@api_view(['GET'])
def api_object_setter(request):
    count = int(request.GET.get('count'))
    sensor_x = Sensor.objects.get(id=int(request.GET.get('sensor_x')))
    sensor_y = Sensor.objects.get(id=int(request.GET.get('sensor_y')))
    ai_mean_x = list((sensor_x.data_sensor.order_by('-date')[:count]).values_list('ai_mean', flat=True))
    ai_mean_y = list((sensor_y.data_sensor.order_by('-date')[:count]).values_list('ai_mean', flat=True))
    out = []
    for x, y in zip(ai_mean_x, ai_mean_y):
        out.append({'x': x, 'y': y})
    max_point = max(ai_mean_x) if max(ai_mean_y) < max(ai_mean_x) else max(ai_mean_y)
    min_point = min(ai_mean_x) if min(ai_mean_y) > min(ai_mean_x) else min(ai_mean_y)
    out.append({'x': max_point, 'y': max_point})
    out.append({'x': min_point, 'y': min_point})
    context = out
    return JsonResponse(context, safe=False)


@api_view(['GET'])
def api_confirm_error(request):
    error_log = SensorError.objects.get(id=int(request.GET.get('error_log_id')))
    if user_access_sensor_read(request, error_log.id_sensor.id):
        error_log.confirmed = True
        error_log.date_of_confirmation = timezone.now()
        error_log.save()
        return JsonResponse({'': True}, safe=False)
    return JsonResponse({'': False}, safe=False)
