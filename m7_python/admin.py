from django.contrib import admin
from .models import UserProfile, Region, Comuna, ContactForm, Inmueble, Solicitud
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Region)
admin.site.register(Comuna)
admin.site.register(ContactForm)
admin.site.register(Inmueble)
admin.site.register(Solicitud)