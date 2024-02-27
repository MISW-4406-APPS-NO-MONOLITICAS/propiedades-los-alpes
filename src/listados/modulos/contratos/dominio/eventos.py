from __future__ import annotations
from dataclasses import dataclass, field
from listados.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime

@dataclass
class TransaccionCreada(EventoDominio):
    id_transaccion: uuid.UUID = None
    valor: float = None
    fecha_creacion: datetime = None