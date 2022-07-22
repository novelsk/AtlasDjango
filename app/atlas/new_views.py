from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.decorators import api_view

from .forms import ObjectEditForm
from .logical import get_objects_and_sensors, user_access_object_write_new
from .models import Sensor, SensorError, Object, ObjectEvent


@login_required
def index(request):
    return render(request, 'new/index.html')


@login_required
def trend(request):
    return render(request, 'new/trend.html', get_objects_and_sensors(request))


@login_required
def analytics(request):
    return render(request, 'new/analytics.html', get_objects_and_sensors(request))


@login_required
def scheme(request):
    return render(request, 'new/scheme.html', get_objects_and_sensors(request))


@login_required
def archive(request):
    context = {}
    object_item = get_object_or_404(Object, pk=int(request.GET.get('object_id')))
    context['object'] = object_item
    errors = SensorError.objects.filter(id_sensor__id_object=object_item).order_by('-error_start_date')[:40]
    context['errors_list'] = list(errors)
    return render(request, 'new/archive.html', context)


@login_required
def object_events(request):
    context = {}
    object_item = get_object_or_404(Object, pk=int(request.GET.get('object_id')))
    context['object'] = object_item
    events = ObjectEvent.objects.filter(id_object=object_item).order_by('-status')
    context['events_list'] = list(events)
    return render(request, 'new/event.html', context)


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
            return render(request, 'new/settings.html', context)
        else:
            form = ObjectEditForm(instance=object_item)
            context['form'] = form
            return render(request, 'new/settings.html', context)
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
