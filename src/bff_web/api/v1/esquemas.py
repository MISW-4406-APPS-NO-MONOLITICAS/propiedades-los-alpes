import typing
import strawberry
import uuid
import requests
import os
from datetime import datetime


CONTRATOS_HOST = os.getenv("CONTRATOS_ADDRESS", default="localhost")
#FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'
FORMATO_FECHA = '%a, %d %b %Y %H:%M:%S %Z'

def obtener_transacciones(root) -> typing.List["Transaccion"]:
    transacciones_json = requests.get(f'http://{CONTRATOS_HOST}:5000/contratos').json()
    transacciones = []
    for transaccion in transacciones_json:
        transacciones.append(
            Transaccion(
                id=transaccion.get('id'),
                id_propiedad=transaccion.get('id_propiedad',''),
                id_auditoria=transaccion.get('id_auditoria',''),
                id_correlacion=transaccion.get('id_correlacion',''),
                fecha_creacion=datetime.strptime(transaccion.get('fecha_creacion'), FORMATO_FECHA), 
                fecha_actualizacion=datetime.strptime(transaccion.get('fecha_actualizacion'), FORMATO_FECHA), 
                valor=transaccion.get('valor').get('valor',''),
                comprador=transaccion.get('comprador', ''),
                vendedor=transaccion.get('vendedor', ''),
                inquilino=transaccion.get('inquilino', ''),
                arrendatario=transaccion.get('arrendatario', '')
            )
        )

    return transacciones

@strawberry.type
class Transaccion:
    id:str
    id_propiedad: str
    id_auditoria: str
    id_correlacion: str
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
