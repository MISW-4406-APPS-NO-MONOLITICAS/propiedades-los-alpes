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
    contrato_id: str

class ObtenerAuditoriasContratoHandler(QueryHandler):
    def handle(self, query: ObtenerAuditoriasContrato) -> QueryResultado:
        repositorio = RepositorioAnalisisDB()        
        return QueryResultado(repositorio.obtener_por_columna('contrato_id', query.contrato_id))


@query.register(ObtenerAuditoriasContrato)
def ejecutar_query_obtener_auditorias_contrato(query: ObtenerAuditoriasContrato):
    handler = ObtenerAuditoriasContratoHandler()
    return handler.handle(query)
