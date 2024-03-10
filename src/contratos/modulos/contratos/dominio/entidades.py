from __future__ import annotations
from contratos.config.logger import logger
from dataclasses import dataclass, field
from uuid import uuid4
from contratos.modulos.contratos.dominio.objetos_valor import Valor

from contratos.seedwork.dominio.entidades import AgregacionRaiz
from contratos.modulos.contratos.dominio.eventos import (
    TransaccionAuditada,
    TransaccionCreada,
)
from contratos.modulos.contratos.aplicacion.eventos.schemas import (
    TransaccionCreadaIntegracion,
)


@dataclass
class Transaccion(AgregacionRaiz):
    id_propiedad: str = field(default_factory=str)
    valor: Valor = field(default_factory=Valor)
    comprador: str = field(default_factory=str)
    vendedor: str = field(default_factory=str)
    inquilino: str = field(default_factory=str)
    arrendatario: str = field(default_factory=str)
    id_auditoria: str | None = None

    def crear_transaccion(self, id_correlacion: str):
        logger.info(
            f"Creando transaccion, agregando evento de dominio {type(TransaccionCreada).__name__}"
        )
        self.agregar_evento(
            TransaccionCreada(
                id_transaccion=self.id, fecha_creacion=self.fecha_creacion
            )
        )

        self.agregar_evento_integracion(
            evento=TransaccionCreadaIntegracion(
                id=str(uuid4()),
                id_correlacion=id_correlacion or str(uuid4()),
                id_transaccion=self.id.__str__(),
                id_propiedad=self.id_propiedad,
                valor=self.valor.valor,
                comprador=self.comprador,
                vendedor=self.vendedor,
                inquilino=self.inquilino,
                intermediario='prueba',
                fecha_evento=self.fecha_creacion.isoformat(),
                fecha_creacion=self.fecha_creacion.isoformat(),
            ),
        )

    def auditar(self, id_auditoria: str):
        self.id_auditoria = id_auditoria
        self.agregar_evento(
            TransaccionAuditada(id_transaccion=self.id, id_auditoria=id_auditoria)
        )
