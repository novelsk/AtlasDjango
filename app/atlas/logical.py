from django.db.models import QuerySet

from .models import AtlasUser, Company, UserAccessGroups, Sensor


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


def user_access_sensor(request, sensor_id):
    """
    Проверяет наличие доступа к изменению настроек датчика
    """
    company = Sensor.objects.get(pk=sensor_id).id_object.id_company
    groups = user_access_company(request, company)
    if groups is not None:
        for i in groups:
            # i = i  # type: UserAccessGroups
            if i.write:
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
                if sensor.error_sensor.count():
                    alerts.append({
                        'style': 'alert-info',
                        'head': sensor.name,
                        'body': 'Ошибок датчика: ' + str(sensor.error_sensor.count()),
                        'href': f'/object/{object_item.id}/{sensor.id}',
                    })
    return alerts
