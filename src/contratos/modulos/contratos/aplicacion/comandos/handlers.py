from contratos.modulos.contratos.aplicacion.dto import TransaccionDTO
from contratos.modulos.contratos.aplicacion.mapeadores import MapeadorCrearTransaccion
from contratos.modulos.contratos.dominio.objetos_valor import Valor
from contratos.modulos.contratos.infraestructura.repositorios import (
    RepositorioTrasaccionesDB,
)
from contratos.modulos.sagas.saga import ManejadorDeSaga
from contratos.seedwork.aplicacion.comandos import ComandoHandler
from contratos.config.logger import logger
from contratos.modulos.contratos.aplicacion.fabricas import FabricaTransacciones
from contratos.seedwork.aplicacion.comandos import ejecutar_commando as comando

from contratos.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from contratos.modulos.contratos.aplicacion.comandos.schemas import (
    ComandoCrearContrato,
    ComandoAuditarContrato,
)


class ComandoCrearContratoHandler(ComandoHandler):
    def __init__(self, db_session=None):
        self.fabrica_transacciones = FabricaTransacciones(
            mapeador=MapeadorCrearTransaccion()
        )
        self.repositorio_transaciones = RepositorioTrasaccionesDB(db_session=db_session)

    def handle(self, comando: ComandoCrearContrato):
        id_correlacion = comando.id_correlacion.__str__()
        logger.info(
            f"Manejando comando %s con id_correlacion %s",
            comando.__class__.__name__,
            id_correlacion,
        )

        transaccion_dto = TransaccionDTO(
            valor=Valor(comando.valor),  # type: ignore
            comprador=comando.comprador,
            vendedor=comando.vendedor,
            inquilino=comando.inquilino,
            arrendatario=comando.arrendatario,
        )
        transaccion = self.fabrica_transacciones.crear_objeto(transaccion_dto)
        transaccion.crear_transaccion()

        logger.info(
            f"Inscribiendo en unidad de trabajo del comando {comando.__class__.__name__}"
        )
        UnidadTrabajoPuerto.registrar_batch(
            self.repositorio_transaciones.agregar, transaccion
        )
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()

        # Iniciamos la saga
        comando_inicial = ComandoAuditarContrato(id_correlacion=comando.id_correlacion)
        ManejadorDeSaga().iniciar_saga(
            id_correlacion=id_correlacion, comando_inicial=comando_inicial
        )


@comando.register(ComandoCrearContrato)
def ejecutar_comando_crear_transaccion(comando: ComandoCrearContrato):
    handler = ComandoCrearContratoHandler()
    handler.handle(comando)
