import time
import os
import datetime
import requests
import json
from fastavro.schema import parse_schema
from pulsar.schema import *
import pulsar.schema as schema

epoch = datetime.datetime.utcfromtimestamp(0)
PULSAR_ENV: str = 'BROKER_HOST'

def time_millis():
    return int(time.time() * 1000)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

def millis_a_datetime(millis):
    return datetime.datetime.fromtimestamp(millis/1000.0)

def broker_host():
    return os.getenv(PULSAR_ENV, default="localhost")

def consultar_schema_registry(topico: str) -> dict:
    json_registry = requests.get(f'http://{broker_host()}:8080/admin/v2/schemas/{topico}/schema').json()
    return json.loads(json_registry.get('data',{}))

def obtener_schema_avro_de_diccionario(json_schema: dict) -> AvroSchema:
    definicion_schema = parse_schema(json_schema)
    return AvroSchema(None,schema_definition=definicion_schema)

class Comando(schema.Record):
    id_correlacion = schema.String(required=True)
    def topic_name(self) -> str:
        raise ValueError("La subclase debe implementar el método topic_name")


class ComandoCrearContrato(Comando):
    id_correlacion = schema.String(required=True)
    id_propiedad = schema.String(required=True)
    valor = schema.Float(required=True)
    comprador = schema.String()
    vendedor = schema.String()
    inquilino = schema.String()
    arrendatario = schema.String()

    def as_dict(self):
        return {
            "id_correlacion": self.id_correlacion,
            "id_propiedad": self.id_propiedad,
            "valor": self.valor,
            "comprador": self.comprador,
            "vendedor": self.vendedor,
            "inquilino": self.inquilino,
            "arrendatario": self.arrendatario,
        }

    def topic_name(self) -> str:
        return "contratos_crear"