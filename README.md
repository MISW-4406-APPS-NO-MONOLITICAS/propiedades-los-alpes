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

### Levantar la base de datos

```bash
docker compose --profile database up -d
```

### Ejecutar cliente que crea una transacción

```bash
python src/listados/api/cliente.py
```

### Revisar contenidos de la base de datos

```bash
mysql -u root -p -h 127.0.0.1 -P 3306 -D listados 
```

Luego SQL

```sql
select * from listados.transacciones;
```

## Escenarios de calidad

Los atributos y escenarios de calidad priorizados para este desarrollo son los encontrados en [el siguiente documento](https://drive.google.com/file/d/16Y6xnwHJ_i88_a9BrG8Z5BUw_KjdHqWL/view?usp=sharing)