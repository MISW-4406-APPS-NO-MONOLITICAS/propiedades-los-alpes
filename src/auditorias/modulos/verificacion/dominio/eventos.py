from __future__ import annotations
from dataclasses import dataclass, field
import uuid

from auditorias.seedwork.dominio.eventos import EventoDominio
from datetime import datetime


@dataclass
class ContratoAuditado(EventoDominio):
    id_correlacion: str = field(default="")
    id_transaccion: str = field(default="")
    id_auditoria: uuid.UUID = field(default_factory=uuid.uuid4)

@dataclass
class ContratoRechazado(EventoDominio):
    id_correlacion: str = field(default="")
    id_transaccion: str = field(default="")    
    
@dataclass
class ContratoAuditadoCancelado(EventoDominio):
    id_correlacion: str = field(default="")
    id_transaccion: str = field(default="")
    
