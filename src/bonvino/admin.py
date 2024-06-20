from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import RegionVitivinicola, Provincia, Pais, Maridaje, NovedadEvento, Bodega, Vino, Varietal, TipoUva, Reseña, Enofilo, Sommelier, Certificacion, CobroPremium, Siguiendo

# Register your models here.

@admin.register(RegionVitivinicola)
class RegionVitivinicolaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')

@admin.register(Provincia)
class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'region_vitivinicola')

@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

@admin.register(Maridaje)
class MaridajeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')

@admin.register(NovedadEvento)
class NovedadEventoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombreEvento', 'descripcion', 'fechaHoraEvento', 'esSoloPremium', 'codigoDescuentoPremium')

@admin.register(Bodega)
class BodegaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'region_vitivinicola', 'coordenadasUbicacion', 'periodoActualizacion')

@admin.register(Vino)
class VinoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'añada', 'precioARS', 'bodega', 'fechaActualizacion')
    filter_horizontal = ('maridajes',)

@admin.register(Varietal)
class VarietalAdmin(admin.ModelAdmin):
    list_display = ('id', 'vino', 'descripcion', 'porcentajeComposicion', 'tipo_uva')

@admin.register(TipoUva)
class TipoUvaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')

@admin.register(Reseña)
class ReseñaAdmin(admin.ModelAdmin):
    list_display = ('id', 'vino', 'usuario', 'fechaReseña', 'puntaje', 'esPremium')

@admin.register(Enofilo)
class EnofiloAdmin(UserAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'apellido', 'get_premium')  # Agregamos get_premium como método
    filter_horizontal = ('favoritos',)  # Eliminamos amigos aquí debido a la restricción

    def get_premium(self, obj):
        return obj.premium
    get_premium.short_description = 'premium'

@admin.register(Sommelier)
class SommelierAdmin(UserAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'fechaValidacion', 'notaPresentacion')

@admin.register(Certificacion)
class CertificacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'institucionOtorgante', 'fechaInicio', 'fechaFin')

@admin.register(CobroPremium)
class CobroPremiumAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fechaPago', 'monto', 'esAnual', 'nroOperacionMercadoPago')

@admin.register(Siguiendo)
class SiguiendoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'amigo', 'bodega', 'sommelier', 'fechaInicio', 'fechaFin')
