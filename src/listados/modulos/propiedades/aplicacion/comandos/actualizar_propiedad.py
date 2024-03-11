
from dataclasses import dataclass, field
from listados.config.logger import logger
from .base import BaseHandler
from listados.seedwork.aplicacion.comandos import Comando
from listados.seedwork.aplicacion.comandos import ejecutar_commando as comando
from listados.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from listados.modulos.propiedades.aplicacion.dto import ActualizarPropiedadDTO, Valor
import pulsar.schema as schema

class ComandoActualizarPropiedad(Comando):
    id_propiedad = schema.String(required=True)
    estado = schema.Boolean(required=True)
    fecha_actualizacion = schema.String(required=True)
    id_transaccion = schema.String(required=True)
    id_correlacion = schema.String(required=True)

    def topic_name(self):
        return "arrendamiento_realizado"
    
    
class ComandoActualizarPropiedadHandler(BaseHandler):
    def handle(self, comando: ComandoActualizarPropiedad):
        logger.info(f"Manejando comando {comando.__class__.__name__}")
        propiedad_dto = ActualizarPropiedadDTO(
            id_propiedad=str(comando),
            estado=bool(comando.estado),
            fecha_actualizacion=str(comando.fecha_actualizacion),
        )
        propiedad = self.fabrica_propiedades.crear_objeto(propiedad_dto)
        propiedad.actualizar_propiedad(str(comando.id_propiedad) ,str(comando.id_correlacion), str(comando.id_transaccion)) # Genera los eventos

        # Se programa en el uow
        logger.info(f"Inscribiendo en unidad de trabajo del comando {comando.__class__.__name__}")
        UnidadTrabajoPuerto.registrar_batch(
            self.repositorio_propiedades.actualizar, propiedad
        )
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(ComandoActualizarPropiedad)
def ejecutar_comando_actualizar_propiedad(comando: ComandoActualizarPropiedad):
    handler = ComandoActualizarPropiedadHandler()
    handler.handle(comando)