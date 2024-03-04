from sqlalchemy import text
from auditorias.config.db import db_session
from auditorias.modulos.verificacion.dominio.repositorios import (
    RepositorioAnalisis,
)
from auditorias.modulos.verificacion.dominio.entidades import (
    Analisis,
)
from auditorias.seedwork.dominio.fabricas import Fabrica
from auditorias.config.logger import logger
from auditorias.seedwork.dominio.repositorios import Mapeador
from .dto import AnalisisDB
from .mapeadores import MapeadorAnalisisDB
from uuid import UUID


class FabricaAnalisisDB(Fabrica):
    def crear_objeto(self, obj, mapeador: Mapeador | None = None) -> Analisis:
        mapeador = mapeador or MapeadorAnalisisDB()
        result = mapeador.dto_a_entidad(obj)
        assert isinstance(result, Analisis)
        return result


logger = logger.getChild("repo-analisises")


class RepositorioTrasaccionesDB(RepositorioAnalisis):
    def __init__(self):
        self._fabrica_analisis: FabricaAnalisisDB = FabricaAnalisisDB()

    @property
    def fabrica_analisis(self):
        return self._fabrica_analisis

    def obtener_por_id(self, id: UUID) -> Analisis | None:
        logger.info(f"Obtaining model with id {id}")
        db_model = db_session.query(AnalisisDB).filter_by(id=str(id)).one_or_none()
        if db_model is None:
            return None
        return self.fabrica_analisis.crear_objeto(db_model)

    def obtener_todos(self) -> list[Analisis]:
        logger.info("Obtaining all models")
        analisises = db_session.query(AnalisisDB).all()
        return [
            self.fabrica_analisis.crear_objeto(analisis)
            for analisis in analisises
        ]

    def agregar(self, entity: Analisis):
        db_model = MapeadorAnalisisDB().entidad_a_dto(entity)
        logger.info(f"Adding model with id {db_model.id}")
        db_session.add(db_model)

    def actualizar(self, entity: Analisis):
        logger.info(f"Updating model with id {entity.id}")
        raise NotImplementedError

    def eliminar(self, entity_id: UUID):
        logger.info(f"Deleting model with id {entity_id}")
        db_session.query(AnalisisDB).filter_by(id=str(entity_id)).delete()

    def obtener_por_columna(self, columna: str, valor: str) -> list[Analisis]:
        analisises = (
            db_session.query(AnalisisDB)
            .where(text(f"{columna} = :valor"))
            .params(valor=valor)
        ).all()
        return [
            self.fabrica_analisis.crear_objeto(analisis)
            for analisis in analisises
        ]
