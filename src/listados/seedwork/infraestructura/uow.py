from abc import ABC, abstractmethod
from enum import Enum
from pydispatch import dispatcher
import pickle

from listados.seedwork.dominio.entidades import AgregacionRaiz


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
            print(f"Publicando evento dominio: {type(evento).__name__}Dominio")
            dispatcher.send(signal=f"{type(evento).__name__}Dominio", evento=evento)

    def _publicar_eventos_post_commit(self):
        for evento in self._obtener_eventos(tipo="integracion"):
            print(f"Publicando evento integracion: {type(evento).__name__}Integracion")
            dispatcher.send(signal="Integracion", evento=evento)


def save_uow(uow):
    try:
        from flask import session
    except:
        raise Exception("Flask is not running, failed to import session")

    session["uow"] = pickle.dumps(uow)


def get_uow() -> UnidadTrabajo:
    try:
        from flask import session
    except:
        raise Exception("Flask is not running, failed to import session")

    if session.get("uow"):
        return pickle.loads(session["uow"])
    else:
        from listados.config.uow import UnidadTrabajoSQLAlchemy

        uow = UnidadTrabajoSQLAlchemy()
        save_uow(uow)
        return uow


class UnidadTrabajoPuerto:
    @staticmethod
    def get_unidad_de_trabajo() -> UnidadTrabajo:
        return get_uow()

    @staticmethod
    def save_unidad_trabajo(uow):
        return save_uow(uow)

    @staticmethod
    def commit():
        uow = __class__.get_unidad_de_trabajo()
        uow.commit()
        __class__.save_unidad_trabajo(uow)

    @staticmethod
    def rollback(savepoint=None):
        uow = __class__.get_unidad_de_trabajo()
        uow.rollback(savepoint=savepoint)
        __class__.save_unidad_trabajo(uow)

    @staticmethod
    def savepoint():
        uow = __class__.get_unidad_de_trabajo()
        uow.savepoint()
        __class__.save_unidad_trabajo(uow)

    @staticmethod
    def dar_savepoints():
        uow = __class__.get_unidad_de_trabajo()
        return uow.savepoints()

    @staticmethod
    def registrar_batch(operacion, *args, lock=Lock.PESIMISTA, **kwargs):
        uow = __class__.get_unidad_de_trabajo()
        uow.registrar_batch(operacion, *args, lock=lock, **kwargs)
        __class__.save_unidad_trabajo(uow)
