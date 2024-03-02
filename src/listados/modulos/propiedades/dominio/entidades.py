from __future__ import annotations
from listados.config.logger import logger
from dataclasses import dataclass, field
from uuid import uuid4
from listados.modulos.propiedades.dominio.objetos_valor import Valor

from listados.seedwork.dominio.entidades import AgregacionRaiz, Entidad
from listados.modulos.propiedades.dominio.eventos import (
    TransaccionCreada,
    TransaccionCreadaIntegracion,
)
from contratos.seedwork.dominio.eventos import EventoIntegracion


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

@dataclass
class