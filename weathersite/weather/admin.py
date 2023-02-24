from django.contrib import admin

from .models import Request, Weather

admin.site.register(Request)
admin.site.register(Weather)
