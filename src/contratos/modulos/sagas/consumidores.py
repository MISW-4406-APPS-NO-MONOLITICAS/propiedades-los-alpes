from auditorias.seedwork.dominio.eventos import EventoIntegracion
from contratos.modulos.sagas.saga import (
    ArrendamientoFallido,
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
        import random

        evento = PropiedadArrendada(id_correlacion=comando.id_correlacion)
        if random.choice([True, False]):
            evento = ArrendamientoFallido(id_correlacion=comando.id_correlacion)

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
