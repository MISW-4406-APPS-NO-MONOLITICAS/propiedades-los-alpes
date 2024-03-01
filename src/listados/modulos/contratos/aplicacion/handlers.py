import uuid
from listados.modulos.contratos.dominio.eventos import TransaccionCreadaIntegracion
from listados.config.logger import logger
from listados.modulos.contratos.infraestructura.repositorios import (
    RepositorioTrasaccionesDB,
)


class TransaccionCreadaIntegracionHandler:
    def __init__(self, event: TransaccionCreadaIntegracion):
        logger.info(
            f"Handling evento {type(event).__name__}, id_transaccion: {event.id_transaccion}"
        )

        repository = RepositorioTrasaccionesDB()
        id_transaccion = uuid.UUID(str(event.id_transaccion))
        found = repository.obtener_por_id(id_transaccion)
        if found:
            logger.info(
                f"Transaccion {event.id_transaccion} ya existe, no se hace nada"
            )
        else:
            logger.info(f"Transaccion {event.id_transaccion} no existe, se crea")
