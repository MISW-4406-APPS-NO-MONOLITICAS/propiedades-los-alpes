from contratos.modulos.sagas.saga import (
    ComandoArrendarPropiedad,
    ContratoAuditado,
    PropiedadArrendada,
)
from contratos.config.pulsar import Consumidor
from contratos.modulos.contratos.aplicacion.comandos.crear_contrato import (
    ComandoAuditarContrato,
)
from contratos.seedwork.dominio.eventos import despachar_evento_integracion


class ComandoAuditarContratoHandler:
    def handle(self, comando: ComandoAuditarContrato):
        evento = ContratoAuditado(id_correlacion=comando.id_correlacion)
        despachar_evento_integracion(evento)


class ComandoArrendarPropiedadHandler:
    def handle(self, comando: ComandoArrendarPropiedad):
        evento = PropiedadArrendada(id_correlacion=comando.id_correlacion)
        despachar_evento_integracion(evento)


consumidores: list[Consumidor] = [
    Consumidor(
        topico=ComandoAuditarContrato().topic_name(),
        mensaje=ComandoAuditarContrato,
        handler=ComandoAuditarContratoHandler().handle,
    ),
    Consumidor(
        topico=ComandoArrendarPropiedad().topic_name(),
        mensaje=ComandoArrendarPropiedad,
        handler=ComandoArrendarPropiedadHandler().handle,
    ),
]
