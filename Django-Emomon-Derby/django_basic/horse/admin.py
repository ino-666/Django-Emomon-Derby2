from django.contrib import admin
from .models import Horse, Trait
from .models import CPU_Horse

admin.site.register(CPU_Horse)
admin.site.register(Horse)
admin.site.register(Trait)