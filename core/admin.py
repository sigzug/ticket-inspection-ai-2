from django.contrib import admin

from core.models import Line, Ride, Station

# Register your models here.
admin.site.register(Line)
admin.site.register(Station)
admin.site.register(Ride)

