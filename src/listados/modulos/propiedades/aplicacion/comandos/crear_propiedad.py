from listados.config.logger import logger
from .base import BaseHandler
from listados.seedwork.aplicacion.comandos import Comando
from listados.seedwork.aplicacion.comandos import ejecutar_commando as comando
from listados.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from listados.modulos.propiedades.aplicacion.dto import PropiedadDTO, Valor
import pulsar.schema as schema

class ComandoCrearPropiedad():
    def __init__(self, id_propiedad, tipo_construccion, estado, area, direccion, lote, compania, fecha_creacion, id_transaccion):
        self.id_propiedad = id_propiedad
        self.tipo_construccion = tipo_construccion
        self.estado = estado
        self.area = area
        self.direccion = direccion
        self.lote = lote
        self.compania = compania
        self.fecha_creacion = fecha_creacion
        self.id_transaccion = id_transaccion

class ComandoCrearPropiedadHandler(BaseHandler):
    def handle(self, comando: ComandoCrearPropiedad):
        logger.info(f"Manejando comando {comando.__class__.__name__}")
        propiedad_dto = PropiedadDTO(
            id=str(comando.id_propiedad),
            tipo_construccion=str(comando.tipo_construccion),
            estado=bool(comando.estado),
            area=float(comando.area),
            direccion=str(comando.direccion),
            lote=str(comando.lote),
            compania=str(comando.compania),
            fecha_registro=str(comando.fecha_creacion),
            fecha_actualizacion=str(comando.fecha_creacion)
        )

        propiedad = self.fabrica_propiedades.crear_objeto(propiedad_dto)
        propiedad.crear_propiedad(str(comando.id_propiedad), str(comando.tipo_construccion), bool(comando.estado), float(comando.area), str(comando.direccion), str(comando.lote), str(comando.compania))

        UnidadTrabajoPuerto.registrar_batch(
            self.repositorio_propiedades.agregar, propiedad
        )
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()                      

