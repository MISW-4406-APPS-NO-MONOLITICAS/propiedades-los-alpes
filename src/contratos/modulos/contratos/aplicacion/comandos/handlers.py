from contratos.modulos.contratos.aplicacion.dto import CrearTransaccionDTO
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
    def __init__(self):
        self.fabrica_transacciones = FabricaTransacciones(
            mapeador=MapeadorCrearTransaccion()
        )
        self.repositorio_transaciones = RepositorioTrasaccionesDB()

    def handle(self, comando: ComandoCrearContrato):
        comando.validate()
        id_correlacion = comando.id_correlacion.__str__()
        logger.info(
            f"Manejando comando %s con id_correlacion %s",
            comando.__class__.__name__,
            id_correlacion,
        )

        transaccion_dto = CrearTransaccionDTO(
            id_propiedad=comando.id_propiedad,
            valor=Valor(comando.valor),  # type: ignore
            comprador=comando.comprador,
            vendedor=comando.vendedor,
            inquilino=comando.inquilino,
            arrendatario=comando.arrendatario,
        )
        transaccion = self.fabrica_transacciones.crear_objeto(transaccion_dto)
        transaccion.crear_transaccion(id_correlacion=id_correlacion)

        logger.info(
            f"Inscribiendo en unidad de trabajo del comando {comando.__class__.__name__}"
        )
        UnidadTrabajoPuerto.registrar_batch(
            self.repositorio_transaciones.agregar, transaccion
        )
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(ComandoCrearContrato)
def ejecutar_comando_crear_transaccion(comando: ComandoCrearContrato):
    handler = ComandoCrearContratoHandler()
    handler.handle(comando)
