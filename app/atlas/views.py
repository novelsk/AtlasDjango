from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from django.http import JsonResponse, QueryDict
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from .forms import LoginForm, UserForm, MLForm, ObjectEventForm, ObjectEventFormEdit, CreateUserForm, ObjectEditForm
from .models import SensorData, SensorError, Sensor, Object, Company, SensorMLSettings, ObjectEvent, AtlasUser
from .logical import user_access_sensor_write, user_access_sensor_read, user_company_view, user_access_object_write
from .util import int_round, int_round_tenth
from .mail import on_error


# old
@login_required
def index(request):
    return render(request, 'index.html')


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
    errors = SensorError.objects.filter(id_sensor__id_object=object_item,
                                        confirmed=False).order_by('-error_start_date')
    context['errors_list'] = list(errors)
    context['errors'] = errors.count()
    return render(request, 'object.html', context)


@login_required
def sensor_chart(request, object_id, sensor_id):
    context = {}
    object_item = Object.objects.get(pk=object_id)
    context['object'] = object_item
    sensor = Sensor.objects.get(pk=sensor_id)
    context['sensor'] = sensor
    errors = SensorError.objects.filter(id_sensor=sensor, confirmed=False).order_by('-error_start_date')
    context['errors_list'] = list(errors)
    context['errors'] = errors.count()
    return render(request, 'sensor.html', context)


@login_required
def archive_object(request, object_id):
    context = {}
    object_item = Object.objects.get(id=object_id)
    context['object'] = object_item
    errors = SensorError.objects.filter(id_sensor__id_object=object_item).order_by('-error_start_date')[:40]
    context['errors_list'] = list(errors)
    return render(request, 'object_errors_arch.html', context)


@login_required
def archive(request, sensor_id):
    context = {}
    sensor = Sensor.objects.get(id=sensor_id)
    context['sensor'] = sensor
    errors = SensorError.objects.filter(id_sensor=sensor).order_by('-error_start_date')[:40]
    context['errors_list'] = list(errors)
    return render(request, 'sensor_errors_arch.html', context)


@login_required
def object_events(request, object_id):
    context = {}
    object_item = Object.objects.get(pk=object_id)
    context['object'] = object_item
    events = ObjectEvent.objects.filter(id_object=object_item).order_by('-status')
    context['events_list'] = list(events)
    return render(request, 'event.html', context)


@login_required
def account(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user, initial={'organization': user_company_view(request)})
        context = {'form': form}
        if form.is_valid():
            form.save()
            form.clean()
            context['success'] = True
        return render(request, 'account.html', context)
    else:
        form = UserForm(instance=request.user, initial={'organization': user_company_view(request)})
        context = {'form': form}
        return render(request, 'account.html', context)


def create_user(request):
    if request.user.is_staff:
        context = {}
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            context['form'] = form
            if form.is_valid():
                AtlasUser.objects.create_user(username=form.cleaned_data['username'],
                                              password=form.cleaned_data['password'],
                                              email=form.cleaned_data['email'])
                context['success'] = True
            return render(request, 'create_user.html', context)
        else:
            form = CreateUserForm()
            context['form'] = form
            return render(request, 'create_user.html', context)
    else:
        return redirect('atlas:index')


def object_settings(request, object_id):
    if user_access_object_write(request, object_id):
        context = {}
        object_item = Object.objects.get(id=object_id)
        context['object'] = object_item
        if request.method == 'POST':
            form = ObjectEditForm(request.POST, instance=object_item, files=request.FILES)
            context['form'] = form
            if form.is_valid():
                form.save()
                context['success'] = True
            return render(request, 'object_settings.html', context)
        else:
            form = ObjectEditForm(instance=object_item)
            context['form'] = form
            return render(request, 'object_settings.html', context)
    else:
        return redirect('atlas:index')


@login_required
def settings_sensor(request, sensor_id):
    context = {}
    sensor = Sensor.objects.get(pk=sensor_id)
    context['sensor'] = sensor
    if not user_access_sensor_write(request, sensor_id):
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
        return render(request, 'sensor_settings.html', context)
    else:
        form = MLForm(instance=settings)
        context['form'] = form
        return render(request, 'sensor_settings.html', context)


@login_required
def event_new(request, object_id):
    context = {}
    object_item = Object.objects.get(pk=object_id)
    context['object'] = object_item

    if request.method == 'POST':
        form = ObjectEventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('atlas:events', object_id)
        context['form'] = form
        return render(request, 'event_new.html', context)
    else:
        form = ObjectEventForm(initial={'id_object': object_item})
        context['form'] = form
        return render(request, 'event_new.html', context)


@login_required
def event_edit(request, event_id):
    context = {}
    event = ObjectEvent.objects.get(pk=event_id)
    context['event'] = event

    if request.method == 'POST':
        form = ObjectEventFormEdit(request.POST, instance=event)
        context['form'] = form
        if form.is_valid():
            form.save()
            form.clean()
            context['success'] = True
        return render(request, 'event_edit.html', context)
    else:
        form = ObjectEventFormEdit(instance=event)
        context['form'] = form
        return render(request, 'event_edit.html', context)


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
            sensor_data = SensorData.objects.create(
                id_sensor=current_sensor, date=data.get('date'), mode=int_round(data.get('mode')),
                ai_max=data.get('ai_max'), ai_min=data.get('ai_min'),
                ai_mean=data.get('ai_mean'), stat_min=data.get('stat_min'),
                stat_max=data.get('stat_max'), ml_min=data.get('ml_min'),
                ml_max=data.get('ml_max'), status=data.get('status'),
            )
            previous_data = SensorData.objects.last()  # type: SensorData
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

            error_mail = False
            if error == 0:
                if previous_data.id_error_log is not None:
                    previous_data.id_error_log.error_end_date = previous_data.date
                    previous_data.id_error_log.save()
            else:
                error_mail = True
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
            # if error_mail:
            #     on_error(sensor_data)
    return JsonResponse(context, safe=False)


@api_view(['GET'])
def api_chart(request, object_id, sensor_id):
    if request.method == 'GET':
        sensor = Sensor.objects.get(id_object__pk=object_id, pk=sensor_id)
        count = int(request.GET.get('count'))
        data_query = sensor.data_sensor.order_by('-date')[:count:-1]  # type: QuerySet
        context = {
            'ai_max': [], 'ai_min': [], 'mode': [],
            'ai_mean': [], 'stat_min': [], 'stat_max': [],
            'ml_min': [], 'ml_max': [], 'date': [],
            'histo_data': [], 'histo_labels': []}
        for data in data_query:
            # data = data  # type: SensorData
            context['ai_max'].append(data.ai_max)
            context['ai_min'].append(data.ai_min)
            context['ai_mean'].append(data.ai_mean)
            context['stat_min'].append(data.stat_min)
            context['stat_max'].append(data.stat_max)
            context['ml_min'].append(data.ml_min)
            context['ml_max'].append(data.ml_max)
            context['mode'].append(data.mode)
            context['date'].append(data.date.astimezone().time())
        temp = list((sensor.data_sensor.order_by('-date')[:count]).values_list('ai_mean', flat=True))
        temp.sort()
        labels = {int_round_tenth(i): 0 for i in temp}
        for i in temp:
            labels[int_round_tenth(i)] += 1
        for key in labels:
            context['histo_data'].append(labels[key])
            context['histo_labels'].append(key)
        return JsonResponse(context, safe=False)


@api_view(['GET'])
def api_object_chart(request, object_id):
    sensors = Sensor.objects.filter(id_object__pk=object_id)
    count = int(request.GET.get('count'))
    context = {'data': [], 'sensors': []}
    for i in sensors:
        # i = i  # type: Sensor
        temp = (i.data_sensor.order_by('-date')[:count]).values_list('ai_mean', flat=True)  # type: QuerySet
        context['data'].append(list(temp)[::-1])
        context['sensors'].append(i.name)
    labels = (sensors.first().data_sensor.order_by('-date')[:count]).values_list('date', flat=True)
    context['labels'] = list(map(lambda x: str(x.astimezone().time()), labels))
    context['labels'].reverse()
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
        error_log.save()
        return JsonResponse({'': True}, safe=False)
    return JsonResponse({'': False}, safe=False)
