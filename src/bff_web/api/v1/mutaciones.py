import strawberry
import typing

from strawberry.types import Info
from bff_web import utils
from bff_web.despachadores import Despachador

from .esquemas import *

@strawberry.type
class Mutation:

    @strawberry.mutation
    async def crear_transaccion(self, valor:float,comprador:str,vendedor:str,inquilino:str,arrendatario:str, info:Info)->TransaccionRespuesta:
        payload = dict(
            valor = valor,
            comprador = comprador,
            vendedor = vendedor,
            inquilino = inquilino,
            arrendatario = arrendatario
        )

        comando = dict(
            id = str(uuid.uuid4()),
            time=utils.time_millis(),
            specversion = "v1",
            type = "ComandoCrearTransaccion",
            ingestion=utils.time_millis(),
            datacontenttype="AVRO",
            service_name = "BFF Web",
            data = payload
        )

        despachador = Despachador()
        info.context["background_tasks"].add_task(
            despachador.publicar_mensaje, 
            comando, 
            "crear_transaccion", 
            "public/default/crear_transaccion"
        )
        
        return TransaccionRespuesta(mensaje="Procesando mensaje",codigo=203)