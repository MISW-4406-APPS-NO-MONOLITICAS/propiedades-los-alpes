from sqlalchemy import text
from listados.config.db import db_session
from listados.modulos.arrendamiento.dominio.repositorios import (
    RepositorioArrendamiento,
)
from listados.modulos.arrendamiento.dominio.entidades import (
    Arrendamiento,
)
from listados.seedwork.dominio.fabricas import Fabrica
from listados.config.logger import logger
from listados.seedwork.dominio.repositorios import Mapeador
from .dto import ArrendamientoDB
from .mapeadores import MapeadorArrendamientoDB
from uuid import UUID


class FabricaArrendamientosDB(Fabrica):
    def crear_objeto(self, obj, mapeador: Mapeador | None = None) -> Arrendamiento:
        mapeador = mapeador or MapeadorArrendamientoDB()
        result = mapeador.dto_a_entidad(obj)
        assert isinstance(result, Arrendamiento)
        return result
    
logger = logger.getChild("repo-arrendamientos")


class RepositorioArrendamientoDB(RepositorioArrendamiento):
    def __init__(self):
        self._fabrica_arrendamientos: FabricaArrendamientosDB = FabricaArrendamientosDB()

    @property
    def fabrica_arrendamientos(self):
        return self._fabrica_arrendamientos

    def obtener_por_id(self, id: UUID) -> Arrendamiento | None:
        logger.info(f"Obtaining model with id {id}")
        db_model = db_session.query(ArrendamientoDB).filter_by(id=str(id)).one_or_none()
        if db_model is None:
            return None
        return self.fabrica_arrendamientos.crear_objeto(db_model)

    def obtener_todos(self) -> list[Arrendamiento]:
        logger.info("Obtaining all models")
        arrendamientos = db_session.query(ArrendamientoDB).all()
        return [
            self.fabrica_arrendamientos.crear_objeto(arrendamiento)
            for arrendamiento in arrendamientos
        ]

    def agregar(self, entity: Arrendamiento):
        db_model = MapeadorArrendamientoDB().entidad_a_dto(entity)
        logger.info(f"Adding model with id {db_model.id}")
        db_session.add(db_model)

    def actualizar(self, entity: Arrendamiento):
        logger.info(f"Updating model with id {entity.id}")


    def eliminar(self, entity_id: UUID):
        logger.info(f"Deleting model with id {entity_id}")
        db_session.query(ArrendamientoDB).filter_by(id=str(entity_id)).delete()


    def obtener_por_columnas(self, columna: str, valor: str) -> list[Arrendamiento]:
        arrendamientos = db_session.query(ArrendamientoDB).filter(text(f"{columna} = '{valor}'")).all()
        return [
            self.fabrica_arrendamientos.crear_objeto(arrendamiento)
            for arrendamiento in arrendamientos
        ]
