from auditorias.config.logger import logger
from auditorias.modulos.verificacion.dominio.eventos import TransaccionCreadaIntegracion


class TransaccionCreadaIntegracionHandler:
    def __init__(self, event: TransaccionCreadaIntegracion):
        logger.info(
            f"Handling evento {type(event).__name__}, id_transaccion: {event.id_transaccion}: {event}"
        )
