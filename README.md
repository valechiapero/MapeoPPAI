# MapeoPPAI
Requisitos:
Instalar Docker y docker compose para poder realizar el tutorial.

Tutorial para instalar Django [Turorial de Django!](https://docs.djangoproject.com/en/2.0/intro/tutorial01/)
Tutorial para crear un entorno virtual de python [Tutorial para crear entorno virtual](https://docs.djangoproject.com/en/2.0/intro/contributing/)

---


Creamos la carpeta donde generaremos nuestra **`app`**. Por ejemplo `fabrica`.
```sh
mkdir fabrica
cd fabrica/
```

Creamos el archivo **`requirements.txt`** para instalar las dependencias en el contenedor, y agregamos lo siguiente.
```
#Framework Django
Django
#Librería para la conexión con PostgreSQL
psycopg2-binary
```

Creamos el archivo **`Dockerfile`** para generar el contenedor donde almacenamos la **`app`**.
```
# Etapa de construcción
FROM python:3.12-alpine AS base
LABEL maintainer="Luciano Parruccia <parruccia@yahoo.com.ar>"
LABEL version="1.0"
LABEL description="cloudset"
RUN apk --no-cache add bash pango ttf-freefont py3-pip curl

# Etapa de construcción
FROM base AS builder
# Instalación de dependencias de construcción
RUN apk --no-cache add py3-pip py3-pillow py3-brotli py3-scipy py3-cffi \
  linux-headers autoconf automake libtool gcc cmake python3-dev \
  fortify-headers binutils libffi-dev wget openssl-dev libc-dev \
  g++ make musl-dev pkgconf libpng-dev openblas-dev build-base \
  font-noto terminus-font libffi

# Copia solo los archivos necesarios para instalar dependencias de Python
COPY ./requirements.txt .

# Instalación de dependencias de Python
RUN pip install --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt \
  && rm requirements.txt

# Etapa de producción
FROM base
RUN mkdir /code
WORKDIR /code
# Copia solo los archivos necesarios desde la etapa de construcción
COPY ./requirements.txt .
RUN pip install -r requirements.txt \
  && rm requirements.txt
COPY --chown=user:group --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages 
#COPY --from=build-python /usr/local/bin/ /usr/local/bin/
ENV PATH /usr/local/lib/python3.12/site-packages:$PATH
# Configuración adicional
RUN ln -s /usr/share/zoneinfo/America/Cordoba /etc/localtime

# Comando predeterminado
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "app.wsgi"]

```

Creamos el archivo **`.env.db`** para almacenar las variables del entorno.
```
#Definimos cada variable
DATABASE_HOST=db
DATABASE_PORT=5432
DATABASE_NAME=postgres
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
# Configuración para inicializar postgres
POSTGRES_PASSWORD=${DATABASE_PASSWORD}
PGUSER=${DATABASE_USER}
PGADMIN_DEFAULT_EMAIL=postgres@postgresql.com
PGADMIN_DEFAULT_PASSWORD=${DATABASE_PASSWORD}
```

Creamos el archivo **`docker compose.yml`** para manipular los contenedores
```
services:
  db:
    image: postgres:alpine
    env_file:
      - .env.db
    environment:
      - POSTGRES_INITDB_ARGS=--auth-host=md5 --auth-local=trust
    healthcheck:
      test: [ "CMD-SHELL", "pg_isready" ]
      interval: 10s
      timeout: 2s
      retries: 5
    volumes:
      - postgres-db:/var/lib/postgresql/data
    networks:
      - net

  backend:
    build: .
    container_name: fabrica_app
    command: runserver 0.0.0.0:8000
    entrypoint: python3 manage.py
    env_file:
      - .env.db
    expose:
      - "8000"
    ports:
      - "8000:8000"
    volumes:
      - ./src:/code
    depends_on:
      db:
        condition: service_healthy
    networks:
      - net

  generate:
    build: .
    command: bash -c 'mkdir src && django-admin startproject app src'
    env_file:
      - .env.db
    volumes:
      - .:/code
    depends_on:
      - db
    networks:
      - net

  manage:
    build: .
    entrypoint: python3 manage.py
    env_file:
      - .env.db
    volumes:
      - ./src:/code
    depends_on:
      - db
    networks:
      - net

networks:
  net:


volumes:
  postgres-db:
```

Generamos la **`app`** que vamos a crear, en nuestro caso **`pastas`** y le damos los permisos necesarios para que se pueda modificar.
```sh
docker compose run --rm generate
docker compose run --rm manage startapp pastas
sudo chown $USER:$USER -R .
```

Realizamos la configuración del archivo **`setting.py`**, y reemplazamos **`nombre`** por el nombre de la app que creamos, en nuestro caso **`pastas`**.
```
#Importamos las librerías
import os

# Permitimos las conexión remota
ALLOWED_HOSTS = [os.environ.get("ALLOWED_HOSTS", "*")]


INSTALLED_APPS = [
    ...
    # agregamos nuestra app al final de la lista
    'pastas',
]
#Configuramos la base de datos
DATABASE_HOST = os.environ.get("DATABASE_HOST", "")
DATABASE_PORT = os.environ.get("DATABASE_PORT", "")
DATABASE_NAME = os.environ.get("DATABASE_NAME", "")
DATABASE_USER = os.environ.get("DATABASE_USER", "")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "")
DATABASES = {
    "default": {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        "ENGINE": "django.db.backends.postgresql",
        # Or path to database file if using sqlite3.
        "NAME": DATABASE_NAME,
        # The following settings are not used with sqlite3:
        "USER": DATABASE_USER,
        "PASSWORD": DATABASE_PASSWORD,
        # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
        "HOST": DATABASE_HOST,
        # Set to empty string for default.
        "PORT": DATABASE_PORT,
    }
}
```

---
## Pasos iniciales para comenzar a trabajar con Django.

Migro la base de datos que se crea por defecto para el proyecto.
```sh
docker compose run manage migrate
```
Para generar un súper usuario de Django
```sh
docker compose run manage createsuperuser
```
Iniciamos los contenedores de la aplicación. El comando ***`-d`*** es para ejecutarlo como demonio, si queremos ir viendo el log de los contenedores, eliminamos el ***`-d`***
```sh
docker compose up -d backend
```
Para ingresar a la app accedemos al siguiente url [http://localhost:8000/admin/](http://localhost:8000/admin/)

En caso de tener algún problema, podemos ver el log de los contenedores. Reemplazamos **`nombre`** por el nombre de la app que creamos.
```sh
docker logs -f nombre_app_1
docker logs -f nombre_db_1
```
---
## Comandos útiles.
Para generar las modificaciones de la base de datos ejecutamos:
```sh
docker compose run manage makemigrations
docker compose run manage migrate
```
Para borrar los contenedores del proyecto:
```sh
docker compose down
```
Para el caso que deseamos eliminar todo lo generado por el docker compose, siempre y cuando los contenedores no estén iniciados, ejecutamos:
```sh
docker system prune -a
```
En el caso de tener problemas para modificar o eliminar algún archivo, le cambiamos el propietario con el siguiente comando, y reemplazamos **`user`** por el usuario con el que estamos logueado
```sh
sudo chown $USER:$USER -R .
```
---
## Editando los archivos de la APP
### **`models.py`**
```
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class NombreAbstract(models.Model):
    nombre = models.CharField(
        _('Nombre'),
        help_text=_('Nombre descriptivo'),
        max_length=200,
        # unique=True,
    )

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        return super().save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.nombre)

    class Meta:
        abstract = True
        ordering = ['nombre']


class Localidad(NombreAbstract):
    class Meta:
        verbose_name = 'localidad'
        verbose_name_plural = 'localidades'


class Barrio(NombreAbstract):
    class Meta:
        verbose_name = 'barrio'
        verbose_name_plural = 'barrios'


class Provincia(NombreAbstract):
    class Meta:
        verbose_name = 'provincia'
        verbose_name_plural = 'provincias'


class Producto(NombreAbstract):
    ganancia = models.DecimalField(
        _('Ganancia'),
        max_digits=15,
        decimal_places=2,
        help_text=_('Ganancia del producto, expresado en coeficiente.'),
        default=0
    )
    es_relleno = models.BooleanField(
        _('Es Relleno'),
        help_text=_('Especifica si el producto contiene relleno.'),
        default=False
    )

    @property
    def precio(self):
        total = 0
        for receta in self.recetas.all():
            total += receta.cantidad * receta.ingrediente.costo
        return round(total * self.ganancia, 2)

    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'


class Cliente(NombreAbstract):
    numero_documento = models.BigIntegerField(
        _('numero documento'),
        help_text=_('numero de documento / CUIT'),
        null=True
    )
    direccion = models.CharField(
        _('dirección'),
        help_text=_('dirección del cliente'),
        max_length=200,
        blank=True,
        null=True
    )
    celular = models.BigIntegerField(
        _('Celular'),
        help_text=_(
            'Número de celular con característica del/la administrador/a'),
        blank=True,
        null=True
    )
    telefono = models.BigIntegerField(
        _('teléfono'),
        help_text=_('teléfono fijo'),
        blank=True,
        null=True
    )
    email = models.EmailField(
        _('email'),
        help_text=_('email del cliente'),
        null=True,
        blank=True,
    )
    barrio = models.ForeignKey(
        Barrio,
        verbose_name=_('barrio'),
        help_text=_('barrio donde reside '),
        related_name='%(app_label)s_%(class)s_related',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    localidad = models.ForeignKey(
        Localidad,
        verbose_name=_('localidad'),
        help_text=_('localidad donde reside el cliente'),
        related_name='%(app_label)s_%(class)s_related',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    provincia = models.ForeignKey(
        Provincia,
        verbose_name=_('provincia'),
        help_text=_('provincia donde reside'),
        related_name='%(app_label)s_%(class)s_related',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    user = models.ForeignKey(
        User,
        help_text=_('Usuario con el que se loguea al sistema'),
        verbose_name='usuario',
        related_name='%(app_label)s_%(class)s',
        related_query_name='%(app_label)s_%(class)s',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    def __str__(self):
        return '{} {}'.format(self.nombre, self.numero_documento)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    'numero_documento',
                    'user',
                ],
                name='%(app_label)s_%(class)s_unico'
            ),
        ]


class Venta(models.Model):
    fecha = models.DateField(
        _('fecha'),
        help_text=_('fecha de la venta')
    )
    cliente = models.ForeignKey(
        Cliente,
        verbose_name=_('cliente'),
        help_text=_('cliente que realiza la compra'),
        related_name='compras',
        on_delete=models.PROTECT,
        blank=False,
        null=False
    )

    def __str__(self):
        return '{} {}'.format(self.fecha, self.cliente.nombre)

    class Meta:
        ordering = ['fecha']
        verbose_name = 'venta'
        verbose_name_plural = 'ventas'


class DetalleVenta(models.Model):
    venta = models.ForeignKey(
        Venta,
        verbose_name=_('venta'),
        help_text=_('detalle de la compra'),
        related_name='detalle',
        on_delete=models.PROTECT,
        blank=False,
        null=False
    )
    cantidad = models.DecimalField(
        _('cantidad'),
        max_digits=15,
        decimal_places=2,
        help_text=_('cantidad'),
        blank=True,
        null=True,
        default=None
    )
    producto = models.ForeignKey(
        Producto,
        verbose_name=_('producto'),
        help_text=_('producto'),
        related_name='detalle',
        on_delete=models.PROTECT,
        blank=False,
        null=False
    )


class UnidadMedida(NombreAbstract):
    pass


class Ingrediente(NombreAbstract):
    costo = models.DecimalField(
        _('Costo'),
        max_digits=15,
        decimal_places=2,
        help_text=_('Costo del ingrediente expresado en pesos'),
        default=0
    )
    unidad_medida = models.ForeignKey(
        UnidadMedida,
        related_name='ingredientes',
        on_delete=models.PROTECT,
        help_text=_('Unidad de medida del ingrediente'),
        null=False,
        blank=False,
        default=1
    )

    class Meta:
        verbose_name = _('Ingrediente')
        verbose_name_plural = _('Ingredientes')


class Receta(models.Model):
    cantidad = models.DecimalField(
        _('Cantidad'),
        max_digits=15,
        decimal_places=3,
        help_text=_(
            'Cantidad del ingrediente, expresado en su unidad de medida.'),
        default=0
    )
    ingrediente = models.ForeignKey(
        Ingrediente,
        related_name='recetas',
        on_delete=models.PROTECT,
        help_text=_('Ingrediente de la receta'),
    )
    producto = models.ForeignKey(
        Producto,
        related_name='recetas',
        on_delete=models.PROTECT,
        help_text=_('Producto de la receta'),
    )

    class Meta:
        ordering = ['ingrediente']
        verbose_name = _('Producto')
        verbose_name_plural = _('Productos')
```
### **`admin.py`**

```
from django.contrib import admin
from pastas.models import *
# Register your models here.
admin.site.register(UnidadMedida)
admin.site.register(Ingrediente)
admin.site.register(Barrio)
admin.site.register(Localidad)
admin.site.register(Provincia)
admin.site.register(Cliente)


class RecetaInline(admin.TabularInline):
    model = Receta
    extra = 0


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    inlines = [
        RecetaInline,
    ]
    list_display = (
        'nombre',
        'precio',
    )
    ordering = ['nombre']  # -nombre descendente, nombre ascendente
    search_fields = ['nombre']
    list_filter = (
        'nombre',
    )


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 0


@admin.register(Venta)
class ComprobanteAdmin(admin.ModelAdmin):
    save_on_top = True
    save_as = True
    list_per_page = 20
    date_hierarchy = 'fecha'
    list_display = (
        'fecha',
        'cliente',
    )

    list_filter = (
        'cliente__nombre',
    )

    inlines = [
        DetalleVentaInline]
```
## Realizamos las migraciones a la base de datos y creamos el super usuario.
```sh
docker compose run --rm manage makemigrations
docker compose run --rm manage migrate
```
## Creamos el fixture
Creamos la carpeta dentro del directorio de la aplicación **`fixtures`** y dentro el siguiente archivo
### **`initial_data.json`**
```
[
    {
        "model": "pastas.unidadmedida",
        "pk": 1,
        "fields": {
            "nombre": "KILO"
        }
    },
    {
        "model": "pastas.unidadmedida",
        "pk": 2,
        "fields": {
            "nombre": "UNIDAD"
        }
    },
    {
        "model": "pastas.ingrediente",
        "pk": 1,
        "fields": {
            "nombre": "HARINA",
            "costo": "50.00",
            "unidad_medida": 1
        }
    },
    {
        "model": "pastas.ingrediente",
        "pk": 2,
        "fields": {
            "nombre": "SAL",
            "costo": "50.00",
            "unidad_medida": 1
        }
    },
    {
        "model": "pastas.ingrediente",
        "pk": 3,
        "fields": {
            "nombre": "HUEVO",
            "costo": "10.00",
            "unidad_medida": 2
        }
    },
    {
        "model": "pastas.ingrediente",
        "pk": 4,
        "fields": {
            "nombre": "JAM\u00d3N",
            "costo": "600.00",
            "unidad_medida": 1
        }
    },
    {
        "model": "pastas.ingrediente",
        "pk": 5,
        "fields": {
            "nombre": "QUESO",
            "costo": "250.00",
            "unidad_medida": 1
        }
    },
    {
        "model": "pastas.ingrediente",
        "pk": 6,
        "fields": {
            "nombre": "ESPINACA",
            "costo": "100.00",
            "unidad_medida": 1
        }
    },
    {
        "model": "pastas.producto",
        "pk": 1,
        "fields": {
            "nombre": "TALLARIN",
            "ganancia": "2.00",
            "es_relleno": false
        }
    },
    {
        "model": "pastas.producto",
        "pk": 2,
        "fields": {
            "nombre": "RAVIOLI ESPINACA",
            "ganancia": "3.00",
            "es_relleno": true
        }
    },
    {
        "model": "pastas.producto",
        "pk": 3,
        "fields": {
            "nombre": "SORRENTINO JAM\u00d3N Y QUESO",
            "ganancia": "3.80",
            "es_relleno": true
        }
    },
    {
        "model": "pastas.receta",
        "pk": 1,
        "fields": {
            "cantidad": "0.90",
            "ingrediente": 1,
            "producto": 1
        }
    },
    {
        "model": "pastas.receta",
        "pk": 2,
        "fields": {
            "cantidad": "0.05",
            "ingrediente": 2,
            "producto": 1
        }
    },
    {
        "model": "pastas.receta",
        "pk": 3,
        "fields": {
            "cantidad": "4.00",
            "ingrediente": 3,
            "producto": 1
        }
    },
    {
        "model": "pastas.receta",
        "pk": 4,
        "fields": {
            "cantidad": "0.60",
            "ingrediente": 1,
            "producto": 2
        }
    },
    {
        "model": "pastas.receta",
        "pk": 5,
        "fields": {
            "cantidad": "4.00",
            "ingrediente": 3,
            "producto": 2
        }
    },
    {
        "model": "pastas.receta",
        "pk": 6,
        "fields": {
            "cantidad": "0.30",
            "ingrediente": 6,
            "producto": 2
        }
    },
    {
        "model": "pastas.receta",
        "pk": 7,
        "fields": {
            "cantidad": "0.60",
            "ingrediente": 1,
            "producto": 3
        }
    },
    {
        "model": "pastas.receta",
        "pk": 8,
        "fields": {
            "cantidad": "4.00",
            "ingrediente": 3,
            "producto": 3
        }
    },
    {
        "model": "pastas.receta",
        "pk": 9,
        "fields": {
            "cantidad": "0.15",
            "ingrediente": 4,
            "producto": 3
        }
    },
    {
        "model": "pastas.receta",
        "pk": 10,
        "fields": {
            "cantidad": "0.15",
            "ingrediente": 5,
            "producto": 3
        }
    },
    {
        "model": "pastas.barrio",
        "pk": 1,
        "fields": {
            "nombre": "centro"
        }
    },
    {
        "model": "pastas.barrio",
        "pk": 2,
        "fields": {
            "nombre": "lamadrid"
        }
    },
    {
        "model": "pastas.barrio",
        "pk": 1,
        "fields": {
            "nombre": "ameghino"
        }
    }
]
```

## Cargamos los datos con el siguiente comando
```
docker compose run --rm manage loaddata initial_data
```