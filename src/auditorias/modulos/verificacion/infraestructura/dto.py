from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from sqlalchemy import Float, String, DateTime, Boolean
from auditorias.config.db import Base
import datetime

class AnalisisDB(Base):
    __tablename__ = "analisis"
    id: Mapped[str] = mapped_column(
        String(50),
        primary_key=True,
        nullable=False,
    )
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    fecha_actualizacion: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False
    )
    tipo_analisis: Mapped[str] = mapped_column(String(200), nullable=True)
    id_correlacion: Mapped[str] = mapped_column(String(50), nullable=False)
    id_transaccion: Mapped[str] = mapped_column(String(50), nullable=False)
    oficial: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    consistente: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    completo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    indice_confiabilidad: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    auditado: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
