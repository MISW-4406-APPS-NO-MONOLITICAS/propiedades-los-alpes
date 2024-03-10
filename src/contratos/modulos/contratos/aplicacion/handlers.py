import uuid
from contratos.modulos.contratos.aplicacion.comandos.schemas import ComandoCrearContrato
from contratos.modulos.contratos.aplicacion.eventos.schemas import TransaccionCreadaIntegracion
from contratos.config.logger import logger
from contratos.modulos.contratos.infraestructura.repositorios import (
    RepositorioTrasaccionesDB,
)

class TransaccionCreadaIntegracionHandler:
    def __init__(self, event: TransaccionCreadaIntegracion):
        logger.info(
            f"Handling evento {event.__class__.__name__}, id_transaccion: {event.id_transaccion}"
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
