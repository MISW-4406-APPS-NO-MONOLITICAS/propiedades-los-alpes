# Proyecto de los Alpes - Entrega 3

Microservicio en Flask de un sistema que provee información sobre bienes raíces comerciales. Está diseñado usando DDD y aplicando el patrón CQRS y usando eventos de dominio e integración para la comunicación asíncrona entre componentes internos parte del mismo contexto acotado y sistemas externos.

## Estructura del proyecto

```
├── docker-compose.yml
├── README.md
├── requirements.txt
├── src
│   └── contratos
│       ├── api
│       │   ├── cliente.py
│       │   ├── companias.py
│       │   ├── contratos.py
│       │   ├── __init__.py
│       │   ├── planos.py
│       │   ├── propiedades.py
│       ├── config
│       │   ├── db.py
│       │   ├── __init__.py
│       │   └── uow.py
│       ├── __init__.py
│       ├── modulos
│       │   ├── companias
│       │   │   └── __init__.py
│       │   ├── contratos
│       │   │   ├── aplicacion
│       │   │   │   ├── comandos
│       │   │   │   │   ├── base.py
│       │   │   │   │   ├── crear_transaccion.py
│       │   │   │   ├── dto.py
│       │   │   │   ├── __init.py
│       │   │   │   ├── mapeadores.py
│       │   │   │   └── queries
│       │   │   │       ├── obtener_contrato.py
│       │   │   │       └── obtener_listado_contratos.py
│       │   │   ├── dominio
│       │   │   │   ├── entidades.py
│       │   │   │   ├── eventos.py
│       │   │   │   ├── excepciones.py
│       │   │   │   ├── fabricas.py
│       │   │   │   ├── __init__.py
│       │   │   │   ├── objetos_valor.py
│       │   │   │   ├── reglas.py
│       │   │   │   └── repositorios.py
│       │   │   ├── infraestructura
│       │   │   │   ├── dto.py
│       │   │   │   ├── excepciones.py
│       │   │   │   ├── fabricas.py
│       │   │   │   ├── __init__.py
│       │   │   │   ├── mapeadores.py
│       │   │   │   └── repositorios.py
│       │   │   ├── __init__.py
│       │   ├── __init__.py
│       │   ├── propiedades
│       │   │   ├── aplicacion
│       │   │   │   ├── comandos
│       │   │   │   │   ├── crear_propiedad.py
│       │   │   │   │   ├── __init__.py
│       │   │   │   ├── handlers.py
│       │   │   │   ├── __init__.py
│       │   │   │   └── queries
│       │   │   │       ├── __init__.py
│       │   │   │       ├── obtener_listado_propiedades.py
│       │   │   │       └── obtener_propiedad.py
│       │   │   ├── dominio
│       │   │   │   ├── entidades.py
│       │   │   │   ├── __init__.py
│       │   │   │   └── objetos_valor.py
│       │   │   └── infraestructura
│       │   │       ├── consumidores.py
│       │   │       └── __init__.py
│       └── seedwork
│           ├── aplicacion
│           │   ├── comandos.py
│           │   ├── dto.py
│           │   ├── handlers.py
│           │   ├── __init__.py
│           │   └── queries.py
│           ├── dominio
│           │   ├── entidades.py
│           │   ├── eventos.py
│           │   ├── excepciones.py
│           │   ├── fabricas.py
│           │   ├── __init.py
│           │   ├── mixins.py
│           │   ├── objetos_valor.py
│           │   ├── reglas.py
│           │   └── repositorios.py
│           ├── infraestructura
│           │   ├── __init__.py
│           │   └── uow.py
│           └── presentacion
│               ├── api.py
│               ├── __init__.py
└── requirements.txt
```

- El directorio `/src` cuenta con un directorio llamado `/contratos`, el cual representa el servicio de propiedades que recibe eventos de integración propagados del sistema de AeroAlpes, por medio de un broker de eventos.
- `src/contratos/api/`: contiene la definición de los endpoints de cada uno de los modulos
- `src/contratos/modulos/`: contiene los diferentes modulos del microservcio. 
- `src/contratos/seedwork`: contiene 

## Propiedades de los Alpes

### Levantar los contenedores y servicios

```bash
docker compose --profile full up -d --build
```

### Ejecutar cliente que crea una transacción

```bash
docker exec contratos python src/contratos/api/cliente.py
```

### Ejecutar pruebas

```bash
docker exec -it contratos python -m pytest --maxfail=1 src/contratos/tests/ 
```

### Monitorear los logs para ver que sucede

```bash
docker logs -f contratos
```

### Reiniciar el servicio

```bash
docker restart contratos
```

### Eliminar base de datos y pulsar para recrear todo en limpio

Importante para cuando se cambia el esquema del tópico.

```bash
docker compose --profile full down --volumes
```

### Debugging

Agregar pdb en una linea

```python
__import__('pdb').set_trace()
```

Reiniciar el contenedor

```bash
docker restart --signal=SIGKILL contratos
```

Attach al contendores

```bash
docker attach contratos
```


## Escenarios de calidad

Los atributos y escenarios de calidad priorizados para este desarrollo son los encontrados en [el siguiente documento](https://drive.google.com/file/d/16Y6xnwHJ_i88_a9BrG8Z5BUw_KjdHqWL/view?usp=sharing)
