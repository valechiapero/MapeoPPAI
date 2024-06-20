from django.contrib import admin
from bonvino.models import *

@admin.register(RegionVitivinicola)
class RegionVitivinicolaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre', 'descripcion')

@admin.register(Provincia)
class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'region_vitivinicola')
    search_fields = ('nombre',)
    list_filter = ('region_vitivinicola',)

@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    filter_horizontal = ('provincias',)

@admin.register(Maridaje)
class MaridajeAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre', 'descripcion')

@admin.register(NovedadEvento)
class NovedadEventoAdmin(admin.ModelAdmin):
    list_display = ('nombreEvento', 'fechaHoraEvento', 'esSoloPremium')
    search_fields = ('nombreEvento', 'descripcion')
    list_filter = ('esSoloPremium', 'fechaHoraEvento')

@admin.register(Bodega)
class BodegaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'region_vitivinicola', 'periodoActualizacion')
    search_fields = ('nombre', 'descripcion', 'historia')
    list_filter = ('region_vitivinicola', 'periodoActualizacion')

@admin.register(Vino)
class VinoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'añada', 'bodega', 'precioARS', 'fechaActualizacion')
    search_fields = ('nombre', 'añada', 'notaDeCataBodega')
    list_filter = ('bodega', 'fechaActualizacion')
    filter_horizontal = ('maridajes',)

@admin.register(Varietal)
class VarietalAdmin(admin.ModelAdmin):
    list_display = ('tipo_uva', 'vino', 'porcentajeComposicion')
    search_fields = ('descripcion',)
    list_filter = ('tipo_uva', 'vino')

@admin.register(TipoUva)
class TipoUvaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre', 'descripcion')

@admin.register(Reseña)
class ReseñaAdmin(admin.ModelAdmin):
    list_display = ('vino', 'usuario', 'puntaje', 'fechaReseña', 'esPremium')
    search_fields = ('comentario',)
    list_filter = ('vino', 'usuario', 'esPremium', 'fechaReseña')

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'premium')
    search_fields = ('nombre',)
    list_filter = ('premium',)

@admin.register(Enofilo)
class EnofiloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'premium')
    search_fields = ('nombre', 'apellido')
    list_filter = ('premium',)
    filter_horizontal = ('amigos', 'favoritos')

@admin.register(Sommelier)
class SommelierAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fechaValidacion', 'premium')
    search_fields = ('nombre', 'notaPresentacion')
    list_filter = ('fechaValidacion', 'premium')
    filter_horizontal = ('certificaciones',)

@admin.register(Certificacion)
class CertificacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'institucionOtorgante', 'fechaInicio', 'fechaFin')
    search_fields = ('nombre', 'institucionOtorgante', 'descripcion')
    list_filter = ('institucionOtorgante', 'fechaInicio', 'fechaFin')

@admin.register(CobroPremium)
class CobroPremiumAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'monto', 'fechaPago', 'esAnual')
    search_fields = ('nroOperacionMercadoPago',)
    list_filter = ('esAnual', 'fechaPago')

@admin.register(Siguiendo)
class SiguiendoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'amigo', 'bodega', 'sommelier', 'fechaInicio', 'fechaFin')
    list_filter = ('usuario', 'amigo', 'bodega', 'sommelier', 'fechaInicio', 'fechaFin')