from sqlalchemy import text
from listados.config.db import db_session
from listados.modulos.contratos.dominio.repositorios import (
    RepositorioTransacciones,
)
from listados.modulos.contratos.dominio.entidades import (
    Transaccion,
)
from listados.seedwork.dominio.fabricas import Fabrica
from listados.config.logger import logger
from listados.seedwork.dominio.repositorios import Mapeador
from .dto import TransaccionDB
from .mapeadores import MapeadorTransaccionDB
from uuid import UUID


class FabricaTransaccionesDB(Fabrica):
    def crear_objeto(self, obj, mapeador: Mapeador | None = None) -> Transaccion:
        mapeador = mapeador or MapeadorTransaccionDB()
        result = mapeador.dto_a_entidad(obj)
        assert isinstance(result, Transaccion)
        return result


logger = logger.getChild("repo-transacciones")


class RepositorioTrasaccionesDB(RepositorioTransacciones):
    def __init__(self):
        self._fabrica_transacciones: FabricaTransaccionesDB = FabricaTransaccionesDB()

    @property
    def fabrica_transacciones(self):
        return self._fabrica_transacciones

    def obtener_por_id(self, id: UUID) -> Transaccion | None:
        logger.info(f"Obtaining model with id {id}")
        db_model = db_session.query(TransaccionDB).filter_by(id=str(id)).one_or_none()
        if db_model is None:
            return None
        return self.fabrica_transacciones.crear_objeto(db_model)

    def obtener_todos(self) -> list[Transaccion]:
        logger.info("Obtaining all models")
        transacciones = db_session.query(TransaccionDB).all()
        return [
            self.fabrica_transacciones.crear_objeto(transaccion)
            for transaccion in transacciones
        ]

    def agregar(self, entity: Transaccion):
        db_model = MapeadorTransaccionDB().entidad_a_dto(entity)
        logger.info(f"Adding model with id {db_model.id}")
        db_session.add(db_model)

    def actualizar(self, entity: Transaccion):
        logger.info(f"Updating model with id {entity.id}")
        raise NotImplementedError

    def eliminar(self, entity_id: UUID):
        logger.info(f"Deleting model with id {entity_id}")
        db_session.query(TransaccionDB).filter_by(id=str(entity_id)).delete()

    def obtener_por_columna(self, columna: str, valor: str) -> list[Transaccion]:
        transacciones = (
            db_session.query(TransaccionDB)
            .where(text(f"{columna} = :valor"))
            .params(valor=valor)
        ).all()
        return [
            self.fabrica_transacciones.crear_objeto(transaccion)
            for transaccion in transacciones
        ]
