from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from sqlalchemy import Float, String, DateTime, Integer, Boolean
from listados.config.db import Base
import datetime


class ArrendamientoDB(Base):
    __tablename__ = "arrendamientos"
    id: Mapped[str] = mapped_column(
        String(50),
        primary_key=True,
        nullable=False,
    )
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    fecha_actualizacion: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False
    )
    id_correlacion: Mapped[str] = mapped_column(String(50), nullable=False)
    id_propiedad: Mapped[str] = mapped_column(String(50), nullable=False)
    id_transaccion: Mapped[str] = mapped_column(String(50), nullable=False)
    fecha_evento: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    valor: Mapped[float] = mapped_column(Float, nullable=False)
    inquilino: Mapped[str] = mapped_column(String(50), nullable=False)
    arrendatario: Mapped[str] = mapped_column(String(50), nullable=False)
    