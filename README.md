# Proyecto de los Alpes - Entrega 4

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

- El directorio `/src` cuenta con los directorios `/contratos`, `/auditorias` y `/propiedades` los cuales representan los microservicios definidos para Propiedades de los Alpes. La comunicación entre ellos se realiza a través de eventos de integración propagados del sistema de AeroAlpes, por medio de un broker de eventos basado en Apache Pulsar
- `src/*/api/`: contiene la definición de los endpoints del microservicio
- `src/*/config/`: contiene las configuraciones generales del microservicio 
- `src/*/modulos/`: contiene los diferentes modulos del microservicio. Cada módulo está estructurado en capas de aplicación, dominio e infraestructura
- `src/*/seedwork/`: contiene las estructuras anémicas transversales al microservicio
- `src/*/tests`: contiene test unitarios
- `src/*/Dockerfile`: preparación y ejecución de la aplicación de acuerdo al microservicio correspondiente
- `docker-compose.yml`: orquestación de microservicios, base de datos mysql, pulsar y red interna

## Propiedades de los Alpes

### Levantar los contenedores y servicios

```bash
docker compose --profile full up -d --build
```

### Ejecutar cliente que crea una transacción

```bash
# Generar transacción valida
docker exec contratos python src/contratos/api/cliente.py --transaccion
# Generar transacción inválida para auditoría
docker exec contratos python src/contratos/api/cliente.py --transaccion --valor 0
```

### Ejecutar pruebas

```bash
# contratos
docker exec -it contratos python -m pytest --maxfail=1 src/contratos/tests/ 
# auditorias
docker exec -it auditorias python -m pytest --maxfail=1 src/auditorias/tests/
```

#### Pruebas desde auditoria
```bash
# detener contratos
export TEST_TYPE=rechazo # simula auditoría rechazada
export TEST_TYPE=exitoso # simula auditoría exitosa y su posterior compensación
export TEST_URL_BASE=http://localhost:5002/auditorias
python src/auditorias/api/cliente.py
```

### Monitorear los logs para ver que sucede

```bash
# contratos
docker logs -f contratos
# auditorias
docker logs -f auditorias
```

### Reiniciar el servicio

```bash
# contratos
docker restart contratos
# auditorias
docker restart auditorias
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

Attach al contenedores

```bash
docker attach contratos
```

Nota: reemplazar 'contratos' con el nombre del microservicio requerido

## Pulsar

Namespace por default en modo standalone: ``` public/default ``` 


Listar tópicos 

```bash
docker exec pulsar bin/pulsar-admin topics list public/default 
```

Estado de un tópico 

```bash
docker exec pulsar bin/pulsar-admin topics stats persistent://public/default/topico 
```

subscribirse 

```bash
docker exec pulsar bin/pulsar-client consume -s sub public/default/topico -t Shared -st auto_consume -n 5  
```

## APIs

### Auditoria

```bash
# Obtener análisis de auditoría realizados sobre una transacción <id_transacción>
curl --request "GET" http://localhost:5002/auditorias/contrato/<id_transacción>

# retorna json
[
   {
      "auditado": true|false,
      "completo": true|false,
      "consistente": true|false,
      "fecha_actualizacion": datetime,
      "fecha_creacion": datetime,
      "id": "<id_analisis>",
      "id_correlacion": "<id_correlacion>",
      "id_transaccion": "<id_transaccion>",
      "indice_confiabilidad": 0..1,
      "oficial": true|false,
      "tipo_analisis": "Contrato"|"Contrato-compensacion"
   },
   {
    ...
   }
]

``` 
#### resultados
* análisis de transacción exitosa: 1 registro - ``` tipo_analisis = Contrato, auditado = true ```
* análisis de transacción rechazada: 1 registro ``` tipo_analisis = Contrato, auditado = false ```
* análisis de transacción rollback: 2 registros ``` { tipo_analisis = Contrato, auditado = true }, { tipo_analisis = Contrato-compensacion, auditado = false } ```

## SAGA

### Flujo de operación larga
Se plantea una operación larga en la que se crea un contrato generando una transacción que debe auditarse para garantizar que la información está completa y el índice de confiabilidad es alto, y debe cambiar el estado de una propiedad a través de un arrendamiento

Pasos: 
1. contrato: escucha comando de ComandoCrearContrato  
2. contrato: emite comando ComandoAuditarContrato  
3. auditoría: escucha comando ComandoAuditarContrato  
4. auditoría: emite evento ContratoAuditado  
4.1 auditoría: emite evento ContratoAuditoriaRechazada  
4.2 contrato: actualiza el estado del contrato  
4.3 contrato: finaliza saga revertida.  
5. contrato: escucha evento ContratoAuditado  
6. contrato: emite comando ComandoArrendarPropiedad  
7. listados: escucha comando ComandoArrendarPropiedad  
8. listados: emite evento PropiedadArrendada  
8.1 listados: emite evento PropiedadArrendamientoRechazado  
8.2 contrato: escucha evento PropiedadArrendamientoRechazado y empieza a revertir saga.  
8.3 contrato: emite comando compensación ComandoCancelarContratoAuditado  
8.4 auditoría: escucha comando de compensación ComandoCancelarContratoAuditado  
8.5 auditoría: emite evento ContratoAuditadoCancelado  
8.6 contrato: finaliza la saga revertida  
9. contrato: escucha evento PropiedadArrendada  
10. finaliza la saga como completada  

![Diagrama de Contexto-SAGA drawio](https://github.com/MISW-4406-APPS-NO-MONOLITICAS/propiedades-los-alpes/assets/98927955/8e2ce5d3-cd92-42c9-afe8-8f40cecfdd17)

[Ver SAGA en Draw.io](https://viewer.diagrams.net/?page-id=8BqL5w1kLr_CeNQm_G1R&highlight=0000ff&edit=_blank&layers=1&nav=1&page-id=8BqL5w1kLr_CeNQm_G1R#G1SEoDtM7BW_qL7KysAWG-W4_v_kGHrHuO)

## Escenarios de calidad

Los atributos y escenarios de calidad priorizados para este desarrollo son los encontrados en [el siguiente documento](https://drive.google.com/file/d/1ergvNQD3fY79l_3he4n_UzElMptrbnxj/view?usp=sharing)
