from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from rest_framework.decorators import api_view

from .forms import ObjectEditForm, MLForm, UserForm, CreateUserForm, ObjectEventForm, ObjectEventFormEdit
from .logical import get_objects_and_sensors, user_access_object_write_new, user_access_sensor_write_new, get_sensor, \
    user_access_sensor_read_new, user_company_view
from .models import Sensor, SensorError, Object, ObjectEvent, SensorMLSettings, AtlasUser, Company
from .util import int_round_tenth


@login_required
def index(request):
    return render(request, 'new/index.html')


@login_required
def company(request):
    context = {}
    company_item = get_object_or_404(Company, pk=int(request.GET.get('company_id')))
    context['company'] = company_item
    objects_list = company_item.object_company.order_by('pk')
    context['objects_list'] = list(objects_list)
    return render(request, 'new/company.html', context=context)


@login_required
def object_trend(request):
    return render(request, 'new/object_trend.html', get_objects_and_sensors(request))


@login_required
def object_analytics(request):
    return render(request, 'new/object_analytics.html', get_objects_and_sensors(request))


@login_required
def object_sensors(request):
    return render(request, 'new/object_sensors.html', get_objects_and_sensors(request))


@login_required
def object_scheme(request):
    return render(request, 'new/object_scheme.html', get_objects_and_sensors(request))


@login_required
def object_archive(request):
    context = {}
    object_item = get_object_or_404(Object, pk=int(request.GET.get('object_id')))
    context['object'] = object_item
    errors = SensorError.objects.filter(id_sensor__id_object=object_item).order_by('-error_start_date')[:40]
    context['errors_list'] = list(errors)
    return render(request, 'new/object_archive.html', context)


@login_required
def object_events(request):
    context = {}
    object_item = get_object_or_404(Object, pk=int(request.GET.get('object_id')))
    context['object'] = object_item
    events = ObjectEvent.objects.filter(id_object=object_item).order_by('-status')
    context['events_list'] = list(events)
    return render(request, 'new/object_event.html', context)


@login_required
def object_events_new(request):
    context = {}
    object_item = get_object_or_404(Object, pk=int(request.GET.get('object_id')))
    context['object'] = object_item
    if request.method == 'POST':
        form = ObjectEventForm(request.POST)
        if form.is_valid():
            form.save()
            return object_events(request)
        context['form'] = form
        return render(request, 'new/object_event_new.html', context)
    else:
        form = ObjectEventForm(initial={'id_object': object_item})
        context['form'] = form
        return render(request, 'new/object_event_new.html', context)


@login_required
def object_event_edit(request,):
    context = {}
    event = ObjectEvent.objects.get(pk=request.GET.get('event_id'))
    context['event'] = event

    if request.method == 'POST':
        form = ObjectEventFormEdit(request.POST, instance=event)
        context['form'] = form
        if form.is_valid():
            form.save()
            context['success'] = True
        return render(request, 'new/object_event_edit.html', context)
    else:
        form = ObjectEventFormEdit(instance=event)
        context['form'] = form
        return render(request, 'new/object_event_edit.html', context)


def object_settings(request):
    if user_access_object_write_new(request):
        context = {}
        object_item = Object.objects.get(id=int(request.GET.get('object_id')))
        context['object'] = object_item
        if request.method == 'POST':
            form = ObjectEditForm(request.POST, instance=object_item, files=request.FILES)
            context['form'] = form
            if form.is_valid():
                form.save()
                context['success'] = True
            return render(request, 'new/object_settings.html', context)
        else:
            form = ObjectEditForm(instance=object_item)
            context['form'] = form
            return render(request, 'new/object_settings.html', context)
    return render(request, 'new/object_trend.html', get_objects_and_sensors(request))


@login_required
def sensor_trend(request):
    return render(request, 'new/sensor_trend.html', get_sensor(request))


@login_required
def sensor_errors(request):
    context = {}
    sensor = get_object_or_404(Sensor, pk=int(request.GET.get('sensor_id')))
    context['sensor'] = sensor
    errors = SensorError.objects.filter(id_sensor=sensor, confirmed=False).order_by('-error_start_date')
    context['errors_list'] = list(errors)
    return render(request, 'new/sensor_errors.html', context)


@login_required
def sensor_settings(request):
    context = {}
    sensor = get_object_or_404(Sensor, pk=int(request.GET.get('sensor_id')))
    context['sensor'] = sensor

    if not user_access_sensor_write_new(request):
        return render(request, 'new/sensor_trend.html', get_sensor(request))

    settings = SensorMLSettings.objects.get_or_create(id_sensor=sensor)[0]
    if request.method == 'POST':
        form = MLForm(request.POST, instance=settings)
        context['form'] = form
        if form.is_valid():
            form.save()
            context['success'] = True
        return render(request, 'new/sensor_settings.html', context)
    else:
        form = MLForm(instance=settings)
        context['form'] = form
        return render(request, 'new/sensor_settings.html', context)


@login_required
def account(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user, initial={'organization': user_company_view(request)})
        context = {'form': form}
        if form.is_valid():
            form.save()
            context['success'] = True
        return render(request, 'new/account.html', context)
    else:
        form = UserForm(instance=request.user, initial={'organization': user_company_view(request)})
        context = {'form': form}
        return render(request, 'new/account.html', context)


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
            return render(request, 'new/create_user.html', context)
        else:
            form = CreateUserForm()
            context['form'] = form
            return render(request, 'new/create_user.html', context)
    else:
        return redirect('atlas:new:index')


# api
@api_view(['GET'])
@login_required
def api_object_chart(request):
    object_id = int(request.GET.get('object_id'))
    count = int(request.GET.get('count'))
    sensors = Sensor.objects.filter(id_object__pk=object_id)
    context = {'data': [], 'sensors': []}
    for i in sensors:
        temp = (i.data_sensor.order_by('-date')[:count]).values_list('ai_mean', flat=True)
        context['data'].append(list(temp)[::-1])
        context['sensors'].append(i.name)
    labels = (sensors.first().data_sensor.order_by('-date')[:count]).values_list('date', flat=True)
    context['labels'] = list(map(lambda x: str(x.astimezone().time()), labels))
    context['labels'].reverse()
    return JsonResponse(context, safe=False)


@api_view(['GET'])
@login_required
def api_sensor_chart(request):
    if request.method == 'GET':
        sensor = Sensor.objects.get(pk=int(request.GET.get('sensor_id')))
        count = int(request.GET.get('count'))

        test_slice = sensor.data_sensor.order_by('-date')[:count]
        context = {
            'ai_max': list(reversed(test_slice.values_list('ai_max', flat=True))),
            'ai_min': list(reversed(test_slice.values_list('ai_min', flat=True))),
            'mode': list(reversed(test_slice.values_list('mode', flat=True))),
            'ai_mean': list(reversed(test_slice.values_list('ai_mean', flat=True))),
            'stat_min': list(reversed(test_slice.values_list('stat_min', flat=True))),
            'stat_max': list(reversed(test_slice.values_list('stat_max', flat=True))),
            'ml_min': list(reversed(test_slice.values_list('ml_min', flat=True))),
            'ml_max': list(reversed(test_slice.values_list('ml_max', flat=True))),
            'date': [i.astimezone().time() for i in reversed(test_slice.values_list('date', flat=True))],
            'histo_data': None,
            'histo_labels': None
        }

        temp = list((sensor.data_sensor.order_by('-date')[:count]).values_list('ai_mean', flat=True))
        temp.sort()
        labels = {int_round_tenth(i): 0 for i in temp}
        for i in temp:
            labels[int_round_tenth(i)] += 1
        context['histo_labels'] = [i for i in labels]
        context['histo_data'] = [labels[key] for key in labels]
        return JsonResponse(context, safe=False)


@login_required
def api_sensor_confirm_errors_all(request):
    if user_access_sensor_read_new(request):
        errors = SensorError.objects.filter(id_sensor__id=int(request.GET.get('sensor_id')), confirmed=False)
        for error in errors:
            error.confirmed = True
            error.date_of_confirmation = timezone.now()
            error.save()
        context = {'': True}
        return JsonResponse(context, safe=False)
    return JsonResponse({'': False}, safe=False)
