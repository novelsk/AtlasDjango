from django.contrib import admin
from .models import Ai, Cmn, AtlasUser, Object, ObjectEvent


admin.site.register(Ai)
admin.site.register(Cmn)
admin.site.register(AtlasUser)
admin.site.register(Object)
admin.site.register(ObjectEvent)
