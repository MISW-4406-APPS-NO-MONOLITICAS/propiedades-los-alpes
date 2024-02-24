# Proyecto de los Alpes - Entrega 3

Microservicio en Flask de un sistema que provee información sobre bienes raíces comerciales. Está diseñado usando DDD y aplicando el patrón CQRS y usando eventos de dominio e integración para la comunicación asíncrona entre componentes internos parte del mismo contexto acotado y sistemas externos.

## Estructura del proyecto

```
propiedades-los-alpes/
├── src/
│   ├── listados/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── propiedades.py
│   │   │   ├── contratos.py
│   │   │   ├── planos.py
│   │   │   ├── companias.py
│   │   ├── config/
│   │   │   ├── __init__.py
│   │   │   ├── db.py
│   │   ├── modulos/
│   │   │   ├── propiedades/
│   │   │   │    ├── aplicacion/
│   │   │   │    │   ├── __init__.py
│   │   │   │    │   ├── comandos/
│   │   │   │    │   ├── queries/
│   │   │   │    ├── dominio/
│   │   │   │    │   ├── __init__.py
│   │   │   │    │   ├── entidades.py
│   │   │   │    │   ├── objetos_valor.py
│   │   │   │    ├── infraestructura/
│   │   │   ├── contratos/
│   │   ├── seedwork/
│   │   │   ├── aplicacion/
│   │   │   │    ├── __init__.py
│   │   │   │    ├── comandos.py
│   │   │   │    ├── dto.py
│   │   │   │    ├── queries.py
│   │   │   ├── dominio/
│   │   │   │    ├── __init__.py
│   │   │   │    ├── entidades.py
│   │   │   │    ├── eventos.py
│   │   │   │    ├── excepciones.py
│   │   │   │    ├── fabricas.py
│   │   │   │    ├── objetos_valor.py
│   │   │   │    ├── reglas.py
│   │   │   ├── infraestructura/
│   │   │   │    ├── __init__.py
│   │   │   ├── presentacion/
│   │   │   │    ├── __init__.py
│   │   │   │    ├── api.py
├── tests/
├── docker-compose.yml
├── propiedades-los-alpes.Dockerfile
├── .gitignore
├── .gitpod.yml
├── requirements.txt
├── README.md
```

- El directorio `/src` cuenta con un directorio llamado `/listados`, el cual representa el servicio de propiedades que recibe eventos de integración propagados del sistema de AeroAlpes, por medio de un broker de eventos.
- `src/listados/api/`: contiene la definición de los endpoints de cada uno de los modulos
- `src/listados/modulos/`: contiene los diferentes modulos del microservcio. 
- `src/listados/seedwork`: contiene 

## Propiedades de los Alpes
### Ejecutar Aplicación

Desde el directorio principal ejecute el siguiente comando.

```bash
flask --app src/listados/api run
```

Ejecución en modo DEBUG:

```bash
flask --app src/listados/api --debug run
```

### Ejecutar pruebas

```bash
coverage run -m pytest
```

### Ver reporte de covertura
```bash
coverage report
```

### Crear imagen Docker

Desde el directorio principal ejecute el siguiente comando.

```bash
docker build . -f listados.Dockerfile -t listados/flask
```

### Ejecutar contenedora (sin compose)

Desde el directorio principal ejecute el siguiente comando.

```bash
docker run -p 5000:5000 aeroalpes/flask
```

## Sidecar/Adaptador
### Instalar librerías

En el mundo real es probable que ambos proyectos estén en repositorios separados, pero por motivos pedagógicos y de simpleza, 
estamos dejando ambos proyectos en un mismo repositorio. Sin embargo, usted puede encontrar un archivo `sidecar-requirements.txt`, 
el cual puede usar para instalar las dependencias de Python para el servidor y cliente gRPC.

```bash
pip install -r sidecar-requirements.txt
```

### Ejecutar Servidor

Desde el directorio principal ejecute el siguiente comando.

```bash
python src/sidecar/main.py 
```

### Ejecutar Cliente

Desde el directorio principal ejecute el siguiente comando.

```bash
python src/sidecar/cliente.py 
```


### Ejecutar contenedora (sin compose)

Desde el directorio principal ejecute el siguiente comando.

```bash
docker run -p 50051:50051 aeroalpes/adaptador
```

### Ejecutar contenedora (sin compose)

Desde el directorio principal ejecute el siguiente comando.

```bash
docker run aeroalpes/ui
```

## Docker-compose

Para desplegar toda la arquitectura en un solo comando, usamos `docker-compose`. Para ello, desde el directorio principal, ejecute el siguiente comando:

```bash
docker-compose up
```

Si desea detener el ambiente ejecute:

```bash
docker-compose stop
```

En caso de querer desplegar dicha topología en el background puede usar el parametro `-d`.

```bash
docker-compose up -d
```

## Comandos útiles

### Listar contenedoras en ejecución
```bash
docker ps
```

### Listar todas las contenedoras
```bash
docker ps -a
```

### Parar contenedora
```bash
docker stop <id_contenedora>
```

### Eliminar contenedora
```bash
docker rm <id_contenedora>
```

### Listar imágenes
```bash
docker images
```

### Eliminar imágenes
```bash
docker images rm <id_imagen>
```

### Acceder a una contendora
```bash
docker exec -it <id_contenedora> sh
```

### Kill proceso que esta usando un puerto
```bash
fuser -k <puerto>/tcp
```

### Correr docker-compose usando profiles
```bash
docker-compose --profile <pulsar|listados> up
```
