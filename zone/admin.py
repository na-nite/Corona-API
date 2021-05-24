from django.contrib import admin

# Register your models here.
from zone.models import NationalZone, InternationalZone

admin.site.register(NationalZone)
admin.site.register(InternationalZone)
