from __future__ import annotations
from auditorias.config.logger import logger
from dataclasses import dataclass, field
from auditorias.modulos.verificacion.dominio.eventos import ContratoAuditado, ContratoRechazado, ContratoAuditadoCancelado
from auditorias.modulos.verificacion.dominio.objetos_valor import TipoAnalisis
from auditorias.modulos.verificacion.infraestructura.schema.v1.eventos import ContratoAuditadoIntegracion, ContratoAuditoriaRechazadaIntegracion, ContratoAuditadoCanceladoIntegracion
from auditorias.seedwork.dominio.entidades import AgregacionRaiz

@dataclass
class Analisis(AgregacionRaiz):
    id_correlacion: str = field(default_factory=str)
    id_transaccion: str = field(default_factory=str)
    tipo_analisis: TipoAnalisis = field(default_factory=TipoAnalisis)
    oficial: bool = field(default_factory=bool)
    consistente: bool = field(default_factory=bool)
    completo: bool = field(default_factory=bool)
    indice_confiabilidad: float = field(default_factory=float)
    auditado: bool = field(default_factory=bool)

    def guardar_analisis(self):
        logger.info(
            f"Guardando analisis, agregando evento de dominio {type(ContratoAuditado).__name__}"
        )
        self.agregar_evento(
            ContratoAuditado(
                id_correlacion = self.id_correlacion, 
                id_transaccion = self.id_transaccion, 
                id_auditoria = self.id
            )
        )

        self.agregar_evento_integracion(
            evento=ContratoAuditadoIntegracion(
                fecha_evento = self.fecha_creacion.isoformat(),
                id_correlacion = self.id_correlacion,
                id_transaccion = self.id_transaccion,
                id_auditoria = f"{self.id}"
            ),
        )
        
    def rechazar_contrato(self):
        logger.info(
            f"Rechazando contrato, agregando evento de dominio {type(ContratoRechazado).__name__}"
        )
        self.agregar_evento(
            ContratoRechazado(
                id_correlacion=self.id_correlacion,
                id_transaccion=self.id_transaccion
            )
        )

        self.agregar_evento_integracion(
            evento=ContratoAuditoriaRechazadaIntegracion(
                fecha_evento = self.fecha_creacion.isoformat(),
                id_correlacion = self.id_correlacion,
                id_transaccion = self.id_transaccion,
                id_auditoria = f"{self.id}"
            ),
        )
        
    def cancelar_contrato_auditado(self):
        logger.info(
            f"Guardando cancelación de contrato, agregando evento de dominio {type(ContratoAuditadoCanceladoIntegracion).__name__}"
        )
        self.agregar_evento(
            ContratoAuditadoCancelado(
                id_correlacion = self.id_correlacion,
                id_transaccion = self.id_transaccion
            )
        )
        
        self.tipo_analisis = TipoAnalisis("Contrato-compensacion")

        self.agregar_evento_integracion(
            evento=ContratoAuditadoCanceladoIntegracion(
                fecha_evento = self.fecha_creacion.isoformat(),
                id_correlacion = self.id_correlacion,
                id_transaccion = self.id_transaccion,
                id_auditoria = f"{self.id}"
            ),
        )
        
