from __future__ import annotations
import uuid
from auditorias.config.logger import logger
from dataclasses import dataclass, field
from uuid import uuid4
from auditorias.modulos.verificacion.dominio.eventos import ContratoAuditado, ContratoAuditadoIntegracion
from auditorias.modulos.verificacion.dominio.objetos_valor import TipoAnalisis
from auditorias.seedwork.dominio.entidades import AgregacionRaiz

@dataclass
class Analisis(AgregacionRaiz):
    tipo_analisis: TipoAnalisis = field(default_factory=TipoAnalisis)
    contrato_id: str = field(default_factory=str)
    oficial: bool = field(default_factory=bool)
    consistente: bool = field(default_factory=bool)
    completo: bool = field(default_factory=bool)
    indice_confiabilidad: float = field(default_factory=float)
    auditado: bool = field(default_factory=bool)

    def auditar_contrato(self):
        logger.info(
            f"Auditando contrato, agregando evento de dominio {type(ContratoAuditado).__name__}"
        )
        self.agregar_evento(
            ContratoAuditado(
                id_transaccion=uuid.UUID(self.contrato_id), fecha_creacion=self.fecha_creacion
            )
        )

        self.agregar_evento_integracion(
            evento=ContratoAuditadoIntegracion(
                id=str(uuid4()),
                fecha_evento=self.fecha_creacion.isoformat(),
                fecha_creacion=self.fecha_creacion.isoformat(),
                tipo_analisis=self.tipo_analisis.valor,
                id_transaccion=self.contrato_id,
                oficial=self.oficial,
                consistente=self.consistente,
                completo=self.completo,
                indice_confiabilidad=self.indice_confiabilidad,
                auditado=self.auditado,
            ),
        )
