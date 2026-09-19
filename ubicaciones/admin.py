from django.contrib import admin
from ubicaciones.models import Agencia,Ciudad,Estado
# Register your models here.


admin.site.register(Estado)
admin.site.register(Ciudad)
admin.site.register(Agencia)
