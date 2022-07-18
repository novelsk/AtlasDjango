# from django.db.models import QuerySet
from .models import Object
from .logical import user_company_query, base_alerts


# https://docs.djangoproject.com/en/1.10/_modules/django/template/context/
def base(request):
    if request.user.is_authenticated:
        company_query = user_company_query(request)
        objects = Object.objects.none()  # type: QuerySet
        if company_query is not None:
            for i in company_query:
                objects = objects.union(i.object_company.all())
        objects = objects.order_by('id_company')
        context = {'base_object_list': list(objects),
                   'objects_count': objects.count(),
                   'alerts': list(base_alerts(request))}
        return context
    else:
        return {}
