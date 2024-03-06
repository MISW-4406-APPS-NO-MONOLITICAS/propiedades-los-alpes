import strawberry
import typing

from strawberry.types import Info
from bff_web import utils
from bff_web.despachadores import Despachador

from .esquemas import *

@strawberry.type
class Mutation:

    @strawberry.mutation
    async def crear_transaccion(self)->TransaccionRespuesta:
        return TransaccionRespuesta(mensaje="test",codigo=203)