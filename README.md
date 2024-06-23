# MapeoPPAI
Requisitos:
Instalar Docker y docker compose para poder realizar el tutorial.

Tutorial para instalar Django [Turorial de Django!](https://docs.djangoproject.com/en/2.0/intro/tutorial01/)
Tutorial para crear un entorno virtual de python [Tutorial para crear entorno virtual](https://docs.djangoproject.com/en/2.0/intro/contributing/)

---


Creamos la carpeta donde generaremos nuestra **`app`**. Por ejemplo `mapeoppai`.
```sh
mkdir mapeoppai
cd mapeoppai/
```

Creamos el archivo **`requirements.txt`** para instalar las dependencias en el contenedor, y agregamos lo siguiente.
```
#Framework Django
Django
#Librería para la conexión con PostgreSQL
psycopg2-binary
```

Creamos el archivo **`Dockerfile`** para generar el contenedor donde almacenamos la **`app`**. <br>
Creamos el archivo **`.env.db`** para almacenar las variables del entorno.<br>
Creamos el archivo **`docker compose.yml`** para manipular los contenedores.<br>

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

En caso de tener algún problema, podemos ver el log de los contenedores.
```sh
docker logs -f bonvino_app
docker logs -f mapeoppai-db-1
```

Para borrar los contenedores del proyecto:
```sh
docker compose down
```
Para el caso que deseamos eliminar todo lo generado por el docker compose, <br>
siempre y cuando los contenedores no estén iniciados, ejecutamos:
```sh
docker system prune -a
```
En el caso de tener problemas para modificar o eliminar algún archivo, le cambiamos el propietario con el siguiente comando, y reemplazamos **`user`** por el usuario con el que estamos logueado
```sh
sudo chown $USER:$USER -R .
```
---
## Editamos los archivos de la APP: 

### **`models.py`** : Contiene la estructura de las tablas de la base de datos

### **`admin.py`** : Configura la visualizacion de las tablas desde la vista del del administrador

## Realizamos las migraciones a la base de datos y creamos el super usuario.
```sh
docker compose run --rm manage makemigrations
docker compose run --rm manage migrate
```
## Creamos el fixture
Creamos la carpeta dentro del directorio de la aplicación **`fixtures`** y dentro el siguiente archivo
### **`initial_data.json`**

## Cargamos los datos con el siguiente comando
```
docker compose run --rm manage loaddata initial_data
```
## Comandos útiles.
Para generar las modificaciones de la base de datos ejecutamos:
```sh
docker compose run manage makemigrations
docker compose run manage migrate
```