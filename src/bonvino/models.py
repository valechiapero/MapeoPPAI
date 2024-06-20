from django.db import models

class RegionVitivinicola(models.Model):
    descripcion = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)

class Provincia(models.Model):
    nombre = models.CharField(max_length=255)
    region_vitivinicola = models.ForeignKey(RegionVitivinicola, on_delete=models.CASCADE, related_name='provincias')

class Pais(models.Model):
    nombre = models.CharField(max_length=255)
    provincias = models.ManyToManyField(Provincia, related_name='paises')

class Maridaje(models.Model):
    descripcion = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)

class NovedadEvento(models.Model):
    codigoDescuentoPremium = models.CharField(max_length=255)
    descripcion = models.TextField()
    esSoloPremium = models.BooleanField()
    fechaHoraEvento = models.DateTimeField()
    nombreEvento = models.CharField(max_length=255)

class Bodega(models.Model):
    coordenadasUbicacion = models.CharField(max_length=255)
    descripcion = models.TextField()
    historia = models.TextField()
    nombre = models.CharField(max_length=255)
    periodoActualizacion = models.DateField()
    region_vitivinicola = models.ForeignKey(RegionVitivinicola, on_delete=models.CASCADE, related_name='bodegas')

class Vino(models.Model):
    añada = models.CharField(max_length=255)
    fechaActualizacion = models.DateField()
    imagenEtiqueta = models.ImageField(upload_to='vinos/')
    nombre = models.CharField(max_length=255)
    notaDeCataBodega = models.TextField()
    precioARS = models.DecimalField(max_digits=10, decimal_places=2)
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE, related_name='vinos')
    maridajes = models.ManyToManyField(Maridaje, related_name='vinos')

class Varietal(models.Model):
    descripcion = models.CharField(max_length=255)
    porcentajeComposicion = models.DecimalField(max_digits=5, decimal_places=2)
    vino = models.ForeignKey(Vino, on_delete=models.CASCADE, related_name='varietales')
    tipo_uva = models.ForeignKey('TipoUva', on_delete=models.CASCADE)

class TipoUva(models.Model):
    descripcion = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)

class Reseña(models.Model):
    comentario = models.TextField()
    esPremium = models.BooleanField()
    fechaReseña = models.DateField()
    puntaje = models.IntegerField()
    vino = models.ForeignKey(Vino, on_delete=models.CASCADE, related_name='reseñas')
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='reseñas')

class Usuario(models.Model):
    contraseña = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)
    premium = models.BooleanField()

class Enofilo(Usuario):
    apellido = models.CharField(max_length=255)
    imagenPerfil = models.ImageField(upload_to='perfiles/')
    amigos = models.ManyToManyField('self', through='Siguiendo', symmetrical=False, related_name='seguidores')
    favoritos = models.ManyToManyField(Vino, related_name='enofilos_favoritos')

class Sommelier(Usuario):
    fechaValidacion = models.DateField()
    notaPresentacion = models.TextField()
    certificaciones = models.ManyToManyField('Certificacion', related_name='sommeliers')

class Certificacion(models.Model):
    adjuntoURL = models.URLField()
    descripcion = models.TextField()
    fechaFin = models.DateField()
    fechaInicio = models.DateField()
    institucionOtorgante = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)

class CobroPremium(models.Model):
    esAnual = models.BooleanField()
    fechaPago = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    nroOperacionMercadoPago = models.CharField(max_length=255)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='cobros_premium')

class Siguiendo(models.Model):
    fechaFin = models.DateField()
    fechaInicio = models.DateField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='siguiendo')
    amigo = models.ForeignKey(Enofilo, on_delete=models.CASCADE, related_name='seguido_por', null=True, blank=True)
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE, related_name='seguido_por', null=True, blank=True)
    sommelier = models.ForeignKey(Sommelier, on_delete=models.CASCADE, related_name='seguido_por', null=True, blank=True)
