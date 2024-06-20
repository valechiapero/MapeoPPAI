from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class RegionVitivinicola(models.Model):
    descripcion = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Provincia(models.Model):
    nombre = models.CharField(max_length=255)
    region_vitivinicola = models.ManyToManyField(RegionVitivinicola, related_name='provincias')

    def __str__(self):
        return self.nombre

class Pais(models.Model):
    nombre = models.CharField(max_length=255)
    provincias = models.ManyToManyField(Provincia, related_name='paises')

    def __str__(self):
        return self.nombre

class Maridaje(models.Model):
    descripcion = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class NovedadEvento(models.Model):
    codigoDescuentoPremium = models.CharField(max_length=255)
    descripcion = models.TextField()
    esSoloPremium = models.BooleanField()
    fechaHoraEvento = models.DateTimeField()
    nombreEvento = models.CharField(max_length=255)

    def __str__(self):
        return self.nombreEvento

class Bodega(models.Model):
    coordenadasUbicacion = models.CharField(max_length=255)
    descripcion = models.TextField()
    historia = models.TextField()
    nombre = models.CharField(max_length=255)
    periodoActualizacion = models.DateField()
    region_vitivinicola = models.ForeignKey(RegionVitivinicola, on_delete=models.CASCADE, related_name='bodegas')

    def __str__(self):
        return self.nombre

class Vino(models.Model):
    añada = models.CharField(max_length=255)
    fechaActualizacion = models.DateField()
    nombre = models.CharField(max_length=255)
    notaDeCataBodega = models.TextField()
    precioARS = models.DecimalField(max_digits=10, decimal_places=2)
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE, related_name='vinos')
    maridajes = models.ManyToManyField(Maridaje, related_name='vinos')

    def __str__(self):
        return self.nombre

class Varietal(models.Model):
    descripcion = models.CharField(max_length=255)
    porcentajeComposicion = models.DecimalField(max_digits=5, decimal_places=2)
    vino = models.ForeignKey(Vino, on_delete=models.CASCADE, related_name='varietales')
    tipo_uva = models.ForeignKey('TipoUva', on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion

class TipoUva(models.Model):
    descripcion = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Reseña(models.Model):
    comentario = models.TextField()
    esPremium = models.BooleanField()
    fechaReseña = models.DateField()
    puntaje = models.IntegerField()
    vino = models.ForeignKey(Vino, on_delete=models.CASCADE, related_name='reseñas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reseñas')

    def __str__(self):
        return f'Reseña de {self.vino.nombre} por {self.usuario.username}'

class Enofilo(User):
    apellido = models.CharField(max_length=255)
    imagenPerfil = models.CharField(max_length=255, blank=True)
    amigos = models.ManyToManyField('self', through='Siguiendo', symmetrical=False, related_name='seguidores')
    favoritos = models.ManyToManyField(Vino, related_name='enofilos_favoritos')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Sommelier(User):
    fechaValidacion = models.DateField()
    notaPresentacion = models.TextField()
    certificaciones = models.ManyToManyField('Certificacion', related_name='sommeliers')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Certificacion(models.Model):
    adjuntoURL = models.URLField()
    descripcion = models.TextField()
    fechaFin = models.DateField()
    fechaInicio = models.DateField()
    institucionOtorgante = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class CobroPremium(models.Model):
    esAnual = models.BooleanField()
    fechaPago = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    nroOperacionMercadoPago = models.CharField(max_length=255)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cobros_premium')

    def __str__(self):
        return f'Cobro de Premium para {self.usuario.username}'

class Siguiendo(models.Model):
    fechaFin = models.DateField()
    fechaInicio = models.DateField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='siguiendo')
    amigo = models.ForeignKey(Enofilo, on_delete=models.CASCADE, related_name='seguido_por', null=True, blank=True)
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE, related_name='seguido_por', null=True, blank=True)
    sommelier = models.ForeignKey(Sommelier, on_delete=models.CASCADE, related_name='seguido_por', null=True, blank=True)

    def __str__(self):
        return f'{self.usuario.username} sigue a {self.amigo or self.bodega or self.sommelier}'
