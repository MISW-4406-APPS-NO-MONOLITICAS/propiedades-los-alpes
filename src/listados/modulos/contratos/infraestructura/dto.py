"""DTOs para la capa de infrastructura del dominio de contratos
"""
import uuid
from listados.config.db import db
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table, Float, String, DateTime
import datetime

Base = db.declarative_base()

class Transaccion(db.Model):
    __tablename__ = "transacciones"
    id: Mapped[str] = mapped_column(String(50), primary_key=True, nullable=False, )
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    fecha_actualizacion: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    valor: Mapped[float] = mapped_column(Float, nullable=False)
    comprador: Mapped[str] = mapped_column(String(200), nullable=True)
    vendedor: Mapped[str] = mapped_column(String(200), nullable=True)
    inquilino: Mapped[str] = mapped_column(String(200), nullable=True)
    arrendatario: Mapped[str] = mapped_column(String(200), nullable=True)