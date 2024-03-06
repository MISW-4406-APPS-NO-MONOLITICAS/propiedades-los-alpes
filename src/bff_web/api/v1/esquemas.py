import typing
import strawberry
import uuid
import requests
import os

from datetime import datetime


CONTRATOS_HOST = os.getenv("CONTRATOS_ADDRESS", default="localhost")
FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

def obtener_transacciones()->typing.List["Transaccion"]:
    transacciones_json = requests.get(f'http://{CONTRATOS_HOST}:5000/contratos').json()
    
    return transacciones_json


@strawberry.type
class Transaccion:
    id:str
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    valor: float
    comprador: str
    vendedor: str
    inquilino: str
    arrendatario: str

@strawberry.type
class TransaccionRespuesta:
    mensaje: str
    codigo: int