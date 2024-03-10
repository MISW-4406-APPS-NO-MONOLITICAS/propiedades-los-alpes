import strawberry
import typing
from strawberry.types import Info
from bff_web import utils
from bff_web.despachadores import Despachador

from .esquemas import *

@strawberry.type
class Mutation:

    @strawberry.mutation
    async def crear_transaccion(
        self, valor:float,comprador:str,vendedor:str,inquilino:str,arrendatario:str,id_correlacion:str,id_propiedad:str, info:Info
    )->TransaccionRespuesta:
        payload = utils.ComandoCrearContrato(
            id_correlacion = id_correlacion,
            id_propiedad = id_propiedad,
            valor = valor,
            comprador = comprador,
            vendedor = vendedor,
            inquilino = inquilino,
            arrendatario = arrendatario
        )
        
        despachador = Despachador()
        info.context["background_tasks"].add_task(
            despachador.publicar_comando, 
            payload
        )
        
        return TransaccionRespuesta(mensaje="Procesando mensaje",codigo=203)



