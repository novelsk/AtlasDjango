from django.db.models import QuerySet

from .models import AtlasUser, Company, Object


# https://docs.djangoproject.com/en/1.10/_modules/django/template/context/
def base(request):
    if request.user.is_authenticated:
        company_query = user_company_query(request)
        objects = Object.objects.none()
        if company_query is not None:
            for i in company_query:
                objects = objects.union(i.object_company.all())
        objects = list(objects)
        context = {'base_object_list': objects}
        return context
    else:
        return {}


def user_company_query(request):
    """Возврщает QuerySet компаний, компаний которые доступны пользователю"""
    current_user = AtlasUser.objects.get(pk=request.user.pk)
    user_groups = current_user.useraccessgroups_set.all()
    company_query = Company.objects.none()  # type: QuerySet
    for i in user_groups:
        company_query = company_query.union(i.companys.all())
    if company_query.count() != 0:
        return company_query
    else:
        return None
