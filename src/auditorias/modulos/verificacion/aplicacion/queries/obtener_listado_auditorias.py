""" from auditorias.modulos.auditorias.infraestructura.repositorios import (
    RepositorioTrasaccionesDB,
)
from auditorias.seedwork.aplicacion.queries import (
    QueryHandler,
    QueryResultado,
    ejecutar_query as query,
)
from dataclasses import dataclass


class ObtenerVerificaciones:
    pass

@dataclass
class ObtenerVerificacionesHandler(QueryHandler):
    def handle(self):
        repositorio = RepositorioTrasaccionesDB()
        return QueryResultado(repositorio.obtener_todos())


@query.register(ObtenerVerificaciones)
def ejecutar_query_obtener_transacciones(query: ObtenerVerificaciones):
    handler = ObtenerVerificacionesHandler()
    return handler.handle()
 """