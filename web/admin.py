from django.contrib import admin
from .models import Consulta, UsuarioPermitido   

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "email", "asunto", "categoria", "fecha")
    list_filter = ("categoria", "fecha")
    search_fields = ("nombre", "email", "asunto", "mensaje")


@admin.register(UsuarioPermitido)
class UsuarioPermitidoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "email", "codigo_validacion")
    search_fields = ("nombre", "email")
