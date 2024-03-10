from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, Integer
from contratos.config.db import Base
import datetime


class SagaLogDB(Base):
    __tablename__ = "saga_logs"
    id_correlacion: Mapped[str] = mapped_column(
        String(50),
        primary_key=True,
        nullable=False,
    )
    index: Mapped[int] = mapped_column(Integer, nullable=False)
    length: Mapped[int] = mapped_column(Integer, nullable=False)
    estado: Mapped[str | None] = mapped_column(String(50), nullable=True)
    last_event_processed: Mapped[str | None] = mapped_column(String(200), nullable=True)
    last_command_dispatched: Mapped[str | None] = mapped_column(String(200), nullable=True)
    fecha_creacion: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    fecha_actualizacion: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, onupdate=datetime.datetime.now
    )
