from listados.modulos.propiedades.infraestructura.repositorios import (
    RepositorioTrasaccionesDB,
)
from contratos.seedwork.aplicacion.queries import (
    QueryHandler,
    QueryResultado,
    ejecutar_query as query,
)
from dataclasses import dataclass


class ObtenerTransacciones:
    pass

@dataclass
class ObtenerTransaccionesHandler(QueryHandler):
    def handle(self):
        repositorio = RepositorioTrasaccionesDB()
        return QueryResultado(repositorio.obtener_todos())


@query.register(ObtenerTransacciones)
def ejecutar_query_obtener_transacciones(query: ObtenerTransacciones):
    handler = ObtenerTransaccionesHandler()
    return handler.handle()
