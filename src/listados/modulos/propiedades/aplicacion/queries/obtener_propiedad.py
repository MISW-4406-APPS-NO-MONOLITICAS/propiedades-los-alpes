from listados.modulos.propiedades.infraestructura.repositorios import (
    RepositorioPropiedadesDB,
)
from listados.seedwork.aplicacion.queries import (
    QueryHandler,
    QueryResultado,
    ejecutar_query as query,
)
from dataclasses import dataclass


class ObtenerPropiedad:
    def __init__(self, id):
        self.id = id

@dataclass
class ObtenerPropiedadHandler(QueryHandler):
    def handle(self, id):
        repositorio = RepositorioPropiedadesDB()
        return QueryResultado(repositorio.obtener_por_id(id))


@query.register(ObtenerPropiedad)
def ejecutar_query_obtener_propiedades(query: ObtenerPropiedad):
    handler = ObtenerPropiedadHandler()
    return handler.handle(id)
