
from dataclasses import dataclass, field
from listados.config.logger import logger
from .base import BaseHandler
from listados.seedwork.aplicacion.comandos import Comando
from listados.seedwork.aplicacion.comandos import ejecutar_commando as comando
from listados.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from listados.modulos.propiedades.aplicacion.dto import PropiedadDTO, Valor
import pulsar.schema as schema

class ComandoActualizarPropiedad(Comando):
    id: str
    tipo_construccion: str
    estado: bool
    area: float
    direccion: str
    lote: int
    compania: str
    fecha_registro: str
    fecha_actualizacion: str

    def topic_name(self):
        return "actualizar_propiedad"
    
    def as_dict(self):
        return {
            "id": self.id,
            "tipo_construccion": self.tipo_construccion,
            "estado": self.estado,
            "area": self.area,
            "direccion": self.direccion,
            "lote": self.lote,
            "compania": self.compania,
            "fecha_registro": self.fecha_registro,
            "fecha_actualizacion": self.fecha_actualizacion,
        }
    
class ComandoActualizarPropiedadHandler(BaseHandler):
    def handle(self, comando: ComandoActualizarPropiedad):
        logger.info(f"Manejando comando {comando.__class__.__name__}")
        propiedad_dto = PropiedadDTO(
            id=comando.id,
            tipo_construccion=comando.tipo_construccion,
            estado=comando.estado,
            area=comando.area,
            direccion=comando.direccion,
            lote=comando.lote,
            compania=comando.compania,
            fecha_registro=comando.fecha_registro,
            fecha_actualizacion=comando.fecha_actualizacion,
        )
        propiedad = self.fabrica_propiedades.crear_objeto(propiedad_dto)
        propiedad.actualizar_propiedad()  # Genera los eventos

        # Se programa en el uow
        logger.info(f"Inscribiendo en unidad de trabajo del comando {comando.__class__.__name__}")
        UnidadTrabajoPuerto.registrar_batch(
            self.repositorio_propiedades.agregar, propiedad
        )
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()