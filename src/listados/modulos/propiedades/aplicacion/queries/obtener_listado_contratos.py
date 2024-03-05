from listados.modulos.propiedades.infraestructura.repositorios import (
    RepositorioPropiedadesDB,
)
from contratos.seedwork.aplicacion.queries import (
    QueryHandler,
    QueryResultado,
    ejecutar_query as query,
)
from dataclasses import dataclass


class ObtenerPropiedades:
    pass

@dataclass
class ObtenerPropiedadesHandler(QueryHandler):
    def handle(self):
        repositorio = RepositorioPropiedadesDB()
        return QueryResultado(repositorio.obtener_todos())


@query.register(ObtenerPropiedades)
def ejecutar_query_obtener_propiedades(query: ObtenerPropiedades):
    handler = ObtenerPropiedadesHandler()
    return handler.handle()
