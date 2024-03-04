from __future__ import annotations
from auditorias.config.logger import logger
from dataclasses import dataclass, field
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

""" from __future__ import annotations
from auditorias.config.logger import logger
from dataclasses import dataclass, field
from uuid import uuid4
from auditorias.modulos.verificacion.dominio.objetos_valor import Valor

from auditorias.seedwork.dominio.entidades import AgregacionRaiz, Entidad
from auditorias.modulos.verificacion.dominio.eventos import (
    TransaccionCreada,
    TransaccionCreadaIntegracion,
)
from auditorias.seedwork.dominio.eventos import EventoIntegracion


@dataclass
class Transaccion(AgregacionRaiz):
    valor: Valor = field(default_factory=Valor)
    comprador: str = field(default_factory=str)
    vendedor: str = field(default_factory=str)
    inquilino: str = field(default_factory=str)
    arrendatario: str = field(default_factory=str)

    def crear_transaccion(self):
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
                fecha_evento=self.fecha_creacion.isoformat(),
                id_transaccion=self.id.__str__(),
                valor=self.valor.valor,
                fecha_creacion=self.fecha_creacion.isoformat(),
                comprador=self.comprador,
                vendedor=self.vendedor,
                inquilino=self.inquilino,
            ),
        )
 """