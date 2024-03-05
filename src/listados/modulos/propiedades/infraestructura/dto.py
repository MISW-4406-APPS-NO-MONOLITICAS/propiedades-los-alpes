"""DTOs para la capa de infrastructura del dominio de propiedades
"""
from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from sqlalchemy import Float, String, DateTime
from listados.config.db import Base
import datetime

class PropiedadDB(Base):
    __tablename__ = "propiedades"
    id: Mapped[str] = mapped_column(
        String(50),
        primary_key=True,
        nullable=False,
    )
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    fecha_actualizacion: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    tipo_construccion: Mapped[str] = mapped_column(String(50), nullable=False)
    estado: Mapped[bool] = mapped_column(String(50), nullable=False)
    area: Mapped[float] = mapped_column(Float, nullable=False)
    direccion: Mapped[str] = mapped_column(String(50), nullable=False)
    lote: Mapped[int] = mapped_column(String(50), nullable=False)
    compania: Mapped[str] = mapped_column(String(50), nullable=False)
    


