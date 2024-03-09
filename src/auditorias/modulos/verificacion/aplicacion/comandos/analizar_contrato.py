""" from dataclasses import dataclass, field
from auditorias.config.logger import logger
from .base import BaseHandler
from auditorias.seedwork.aplicacion.comandos import Comando
from auditorias.seedwork.aplicacion.comandos import ejecutar_comando as comando
from auditorias.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from auditorias.modulos.verificacion.aplicacion.dto import AnalisisDTO, TipoAnalisis
import pulsar.schema as schema


class ComandoAnalizarContrato(Comando):
    tipo_analisis = schema.String()
    contrato_id = schema.String()
    oficial = schema.Boolean()
    consistente = schema.Boolean()
    completo = schema.Boolean()
    indice_confiabilidad = schema.Float()
    auditado = schema.Boolean()

    def topic_name(self):
        return "analizar_contrato"

    def as_dict(self):
        return {
            "tipo_analisis": self.tipo_analisis,
            "contrato_id": self.contrato_id,
            "oficial": self.oficial,
            "consistente": self.consistente,
            "completo": self.completo,
            "indice_confiabilidad": self.indice_confiabilidad,
            "auditado": self.auditado
        }


class ComandoAnalizarContratoHandler(BaseHandler):
    def handle(self, comando: ComandoAnalizarContrato):
        logger.info(f"Manejando comando {comando.__class__.__name__}")
        transaccion_dto = AnalisisDTO(
            tipo_analisis=TipoAnalisis(comando.tipo_analisis),
            contrato_id=comando.contrato_id,
            oficial=comando.oficial,
            consistente=comando.consistente,
            completo=comando.completo,
            indice_confiabilidad=comando.indice_confiabilidad,
            auditado=comando.auditado,
        )
        transaccion = self.fabrica_transacciones.crear_objeto(transaccion_dto)
        transaccion.auditar_contrato()  # Genera los eventos

        # Se programa en el uow
        logger.info(f"Inscribiendo en unidad de trabajo del comando {comando.__class__.__name__}")
        UnidadTrabajoPuerto.registrar_batch(
            self.repositorio_transaciones.agregar, transaccion
        )
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(ComandoAnalizarContrato)
def ejecutar_comando_auditar_contrato(comando: ComandoAnalizarContrato):
    handler = ComandoAnalizarContratoHandler()
    handler.handle(comando)
 """