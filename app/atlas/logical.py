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
            # i = i  # type: UserAccessGroups
            if i.write:
                return True
    return False
