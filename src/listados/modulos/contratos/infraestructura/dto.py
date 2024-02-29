"""DTOs para la capa de infrastructura del dominio de contratos
"""
from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from sqlalchemy import Float, String, DateTime
from listados.config.db import db
import datetime

Base = declarative_base()
Model = db.Model


class TransaccionDB(Model):
    __tablename__ = "transacciones"
    id: Mapped[str] = mapped_column(
        String(50),
        primary_key=True,
        nullable=False,
    )
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    fecha_actualizacion: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False
    )
    valor: Mapped[float] = mapped_column(Float, nullable=False)
    comprador: Mapped[str] = mapped_column(String(200), nullable=True)
    vendedor: Mapped[str] = mapped_column(String(200), nullable=True)
    inquilino: Mapped[str] = mapped_column(String(200), nullable=True)
    arrendatario: Mapped[str] = mapped_column(String(200), nullable=True)
