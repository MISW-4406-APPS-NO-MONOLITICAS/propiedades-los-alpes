from pydispatch import dispatcher
from auditorias.modulos.verificacion.dominio.eventos import ContratoAuditado
from auditorias.seedwork.aplicacion.handlers import Handler
from auditorias.config.logger import logger

logger = logger.getChild("propiedades-handler")


class HandlerAnalisisDominio(Handler):
    @staticmethod
    def handle_contrato_auditado(evento):
        logger.info(f"Handling evento de dominio {type(evento).__name__}")


def registrar():
    dispatcher.connect(
        HandlerAnalisisDominio.handle_contrato_auditado,
        signal="ContratoAuditadoDominio",
    )
