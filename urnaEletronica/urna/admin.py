from django.contrib import admin
from .models import Urna, Politico, Eleitor


admin.site.register(Urna)
admin.site.register(Politico)
admin.site.register(Eleitor)
