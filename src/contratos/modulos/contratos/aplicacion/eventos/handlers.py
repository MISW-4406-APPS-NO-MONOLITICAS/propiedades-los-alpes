import uuid
from pydispatch import dispatcher
from contratos.modulos.contratos.aplicacion.eventos.schemas import ContratoAuditado
from contratos.modulos.contratos.infraestructura.repositorios import (
    RepositorioTrasaccionesDB,
)
from contratos.modulos.propiedades.aplicacion.handlers import HandlerTransaccionDominio
from contratos.seedwork.aplicacion.handlers import Handler
from contratos.config.logger import logger
from contratos.seedwork.infraestructura.uow import UnidadTrabajoPuerto

logger = logger.getChild("eventos-integracion-handler")


class HandlerPropiedadAuditada(Handler):
    @staticmethod
    def handle(evento: ContratoAuditado):
        logger.info(
            f"Handling evento %s para transaccion %s e id_correlacion %s",
            evento.__class__.__name__,
            evento.id_transaccion,
            evento.id_correlacion,
        )
        assert isinstance(evento, ContratoAuditado)
        repo = RepositorioTrasaccionesDB()
        transaccion = repo.obtener_por_id(uuid.UUID(evento.id_transaccion.__str__()))
        if not transaccion:
            raise ValueError(f"Transaccion {evento.id_transaccion} no existe")

        transaccion.auditar(evento.id_auditoria.__str__())
        UnidadTrabajoPuerto.registrar_batch(repo.actualizar, transaccion)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()
        logger.info(f"Transaccion {evento.id_transaccion} auditada")


def registrar():
    dispatcher.connect(
        HandlerPropiedadAuditada.handle,
        signal=ContratoAuditado.__name__,
    )
