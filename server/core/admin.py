from django.contrib import admin

# Register your models here.
from .models import AppUser, RideRequest

admin.site.register(AppUser)
admin.site.register(RideRequest)
