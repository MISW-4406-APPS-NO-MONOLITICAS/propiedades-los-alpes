
import strawberry
from .esquemas import *

@strawberry.type
class Query:
    transacciones: typing.List[Transaccion] = strawberry.field(resolver=obtener_transacciones)