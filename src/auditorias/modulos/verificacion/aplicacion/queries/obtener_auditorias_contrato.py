from auditorias.modulos.verificacion.infraestructura.repositorios import RepositorioAnalisisDB
from auditorias.seedwork.aplicacion.queries import (
    Query,
    QueryHandler,
    QueryResultado,
    ejecutar_query as query,
)
from dataclasses import dataclass

@dataclass
class ObtenerAuditoriasContrato(Query):
    id_transaccion: str

class ObtenerAuditoriasContratoHandler(QueryHandler):
    def handle(self, query: ObtenerAuditoriasContrato) -> QueryResultado:
        repositorio = RepositorioAnalisisDB()        
        return QueryResultado(repositorio.obtener_por_columna('id_transaccion', query.id_transaccion))


@query.register(ObtenerAuditoriasContrato)
def ejecutar_query_obtener_auditorias_contrato(query: ObtenerAuditoriasContrato):
    handler = ObtenerAuditoriasContratoHandler()
    return handler.handle(query)
