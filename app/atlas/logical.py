import datetime

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from .models import AtlasUser, Company, UserAccessGroups, Sensor, Object


def user_company_query(request):
    """
    Возврщает QuerySet компаний, компаний которые доступны пользователю
    """
    current_user = AtlasUser.objects.get(pk=request.user.pk)
    user_groups = current_user.useraccessgroups_set.all()
    company_query = Company.objects.none()  # type: QuerySet
    for i in user_groups:
        company_query = company_query.union(i.companys.all())
    if company_query.count() != 0:
        return company_query
    else:
        return None


def user_company_view(request):
    """
    Возврщает назвавние компании пользователя или другой удовл. результат
    """
    companys = user_company_query(request)  # type: QuerySet
    if companys is not None:
        if companys.count() > 1:
            out_text = ''
            for company in companys:
                # company = company  # type: Company
                out_text += company.name + ', '
            return out_text.rstrip(', ')[:50]
        return companys.first().name
    return 'Нет ни в одной организации'


def user_access_company(request, company):
    """
    Возврщает QuerySet групп, доступных пользвоателю, по компании
    """
    groups = UserAccessGroups.objects.filter(users=request.user, companys=company)
    if groups.count() != 0:
        return groups
    else:
        return None


def can_write(groups):
    """
    Проверяет возможность записи из списка групп
    """
    if groups is not None:
        for i in groups:
            if i.write:
                return True
    return False


def user_access_object_write(request, object_id):
    """
    Проверяет наличие доступа к изменению настроек объекта
    """
    company = Object.objects.get(pk=object_id).id_company
    groups = user_access_company(request, company)
    return can_write(groups)


def user_access_object_write_new(request):
    """
    Проверяет наличие доступа к изменению настроек объекта
    """
    company = get_object_or_404(Object, pk=int(request.GET.get('object_id'))).id_company
    groups = user_access_company(request, company)
    return can_write(groups)


def user_access_sensor_write(request, sensor_id):
    """
    Проверяет наличие доступа к изменению настроек датчика
    """
    company = Sensor.objects.get(pk=sensor_id).id_object.id_company
    groups = user_access_company(request, company)
    return can_write(groups)


def user_access_sensor_read(request, sensor_id):
    """
    Проверяет наличие доступа к датчику
    """
    company = Sensor.objects.get(pk=sensor_id).id_object.id_company
    groups = user_access_company(request, company)
    if groups is not None:
        return True
    return False


def base_alerts(request):
    """
    Возвращает список уведомлений
    """
    company_query = user_company_query(request)
    alerts = []
    for company in company_query:
        for object_item in company.object_company.all():
            # object_item = object_item  # type: Object
            if object_item.count_event_not_done():
                alerts.append({
                    'style': 'alert-warning',
                    'head': object_item.name,
                    'body': 'Просроченные мероприятия по объекту: ' + str(object_item.count_event_not_done()),
                    'href': f'/object/{object_item.id}/events',
                    })
            for sensor in object_item.sensor_object.all():
                if sensor.count_alerts():
                    temp = sensor.error_sensor.all().last().error_start_date  # type: datetime.datetime
                    alerts.append({
                        'style': 'alert-info',
                        'head': f'{object_item.name} - {sensor.name}',
                        'body': f'Ошибок датчика: ' + str(sensor.error_sensor.count()),
                        'after': f'Последняя запись: {temp.time()}',
                        'href': f'/object/{object_item.id}/{sensor.id}',
                    })
    return alerts


def get_objects_and_sensors(request):
    """
    Контекст с объектом и датчиками
    """
    context = {}
    object_item = get_object_or_404(Object, pk=int(request.GET.get('object_id')))
    context['object'] = object_item
    sensors = Sensor.objects.filter(id_object=object_item).order_by('id_sensor_repr')
    context['sensors_list'] = list(sensors)
    return context
