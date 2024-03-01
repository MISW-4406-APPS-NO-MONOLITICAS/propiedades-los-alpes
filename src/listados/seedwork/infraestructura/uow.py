from abc import ABC, abstractmethod
from enum import Enum
from pydispatch import dispatcher
from listados.config.logger import logger

from listados.seedwork.dominio.entidades import AgregacionRaiz
from listados.seedwork.dominio.eventos import EventoDominio, EventoIntegracion


class Lock(Enum):
    OPTIMISTA = 1
    PESIMISTA = 2


class Batch:
    def __init__(self, operacion, lock: Lock, *args, **kwargs):
        self.operacion = operacion
        self.args = args
        self.lock = lock
        self.kwargs = kwargs


class UnidadTrabajo:
    batches: list[Batch] = []

    def __enter__(self):
        return self

    def __exit__(self):
        self.rollback()

    def _obtener_eventos(self, batches=None, tipo: str = "dominio"):
        batches = self.batches if batches is None else batches
        for batch in batches:
            for arg in batch.args:
                if isinstance(arg, AgregacionRaiz):
                    if tipo == "dominio":
                        return arg.eventos
                    elif tipo == "integracion":
                        return arg.eventos_integracion
                    else:
                        raise ValueError("Tipo de evento no soportado")

        return []

    @abstractmethod
    def _limpiar_batches(self):
        self.batches = []

    @abstractmethod
    def savepoint(self):
        raise NotImplementedError

    @abstractmethod
    def savepoints(self) -> list:
        raise NotImplementedError

    def commit(self):
        self._publicar_eventos_post_commit()
        self._limpiar_batches()

    @abstractmethod
    def rollback(self, savepoint=None):
        self._limpiar_batches()

    def registrar_batch(self, operacion, *args, lock=Lock.PESIMISTA, **kwargs):
        batch = Batch(operacion, lock, *args, **kwargs)
        self.batches.append(batch)
        self._publicar_eventos_dominio(batch)

    def _publicar_eventos_dominio(self, batch):
        for evento in self._obtener_eventos(tipo="dominio", batches=[batch]):
            assert isinstance(evento, EventoDominio), "Debe ser un evento de dominio"
            logger.info(
                f"Publicando evento dominio: {type(evento).__name__} en signal {type(evento).__name__}Dominio"
            )
            dispatcher.send(signal=f"{type(evento).__name__}Dominio", evento=evento)

    def _publicar_eventos_post_commit(self):
        for evento in self._obtener_eventos(tipo="integracion"):
            assert isinstance(
                evento, EventoIntegracion
            ), "Debe ser un evento de integracion"
            logger.info(
                f"Publicando evento integracion: {evento.evento.__class__.__name__} en signal Integracion"
            )
            dispatcher.send(signal="Integracion", evento=evento)


uow = None


def get_uow():
    global uow
    if uow is None:
        from listados.config.uow import UnidadTrabajoSQLAlchemy

        uow = UnidadTrabajoSQLAlchemy()
    return uow


class UnidadTrabajoPuerto:
    @staticmethod
    def get_unidad_de_trabajo() -> UnidadTrabajo:
        return get_uow()

    @staticmethod
    def commit():
        uow = __class__.get_unidad_de_trabajo()
        uow.commit()

    @staticmethod
    def rollback(savepoint=None):
        uow = __class__.get_unidad_de_trabajo()
        uow.rollback(savepoint=savepoint)

    @staticmethod
    def savepoint():
        uow = __class__.get_unidad_de_trabajo()
        uow.savepoint()

    @staticmethod
    def dar_savepoints():
        uow = __class__.get_unidad_de_trabajo()
        return uow.savepoints()

    @staticmethod
    def registrar_batch(operacion, *args, lock=Lock.PESIMISTA, **kwargs):
        uow = __class__.get_unidad_de_trabajo()
        uow.registrar_batch(operacion, *args, lock=lock, **kwargs)
