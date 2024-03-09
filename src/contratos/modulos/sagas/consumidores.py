import uuid
from auditorias.seedwork.dominio.eventos import EventoIntegracion
from contratos.config.pulsar import Consumidor
from contratos.modulos.contratos.aplicacion.comandos.schemas import (
    ComandoArrendarPropiedad,
    ComandoAuditarContrato,
)
from contratos.modulos.contratos.aplicacion.eventos.schemas import (
    ContratoAuditado,
    PropiedadArrendada,
    PropiedadArrendamientoRechazado,
)
from contratos.seedwork.dominio.eventos import despachar_evento_integracion


class ComandoAuditarContratoHandler:
    def handle(self, comando: ComandoAuditarContrato):
        evento = ContratoAuditado(
            id_correlacion=comando.id_correlacion,
            id_transaccion=comando.id_transaccion,
            id_auditoria=str(uuid.uuid4()),
        )
        despachar_evento_integracion(evento)


class ComandoArrendarPropiedadHandler:
    def handle(self, comando: ComandoArrendarPropiedad):
        import random

        evento = PropiedadArrendada(
            id_correlacion=comando.id_correlacion,
            id_propiedad=comando.id_propiedad,
            id_transaccion=comando.id_transaccion,
        )
        if random.choice([True, False]):
            evento = PropiedadArrendamientoRechazado(
                id_correlacion=comando.id_correlacion
            )

        despachar_evento_integracion(evento)


consumidores: list[Consumidor] = [
    Consumidor(
        mensaje=ComandoAuditarContrato,
        handler=ComandoAuditarContratoHandler().handle,
    ),
    Consumidor(
        mensaje=ComandoArrendarPropiedad,
        handler=ComandoArrendarPropiedadHandler().handle,
    ),
]
