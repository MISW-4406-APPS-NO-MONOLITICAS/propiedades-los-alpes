from pydispatch import dispatcher
from contratos.modulos.contratos.dominio.eventos import TransaccionCreada
from contratos.seedwork.aplicacion.handlers import Handler
from contratos.config.logger import logger

logger = logger.getChild("propiedades-handler")


class HandlerTransaccionDominio(Handler):
    @staticmethod
    def handle_transaccion_creada(evento):
        assert isinstance(evento, TransaccionCreada)
        logger.info(f"Handling evento de dominio {evento.__class__.__name__}")


def registrar():
    dispatcher.connect(
        HandlerTransaccionDominio.handle_transaccion_creada,
        signal="TransaccionCreadaDominio",
    )
