from pydispatch import dispatcher
from listados.modulos.contratos.dominio.eventos import TransaccionCreada
from listados.seedwork.aplicacion.handlers import Handler
from listados.config.logger import logger

logger = logger.getChild("propiedades-handler")


class HandlerTransaccionDominio(Handler):
    @staticmethod
    def handle_transaccion_creada(evento):
        logger.info(f"Handling evento de dominio {type(evento).__name__}")


def registrar():
    dispatcher.connect(
        HandlerTransaccionDominio.handle_transaccion_creada,
        signal="TransaccionCreadaDominio",
    )
