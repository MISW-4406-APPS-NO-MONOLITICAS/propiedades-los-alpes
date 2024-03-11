from sqlalchemy import text
from listados.config.db import db_session
from listados.modulos.propiedades.dominio.repositorios import (
    RepositorioPropiedades,
)
from listados.modulos.propiedades.dominio.entidades import (
    Propiedad,
)
from listados.seedwork.dominio.fabricas import Fabrica
from listados.config.logger import logger
from listados.seedwork.dominio.repositorios import Mapeador
from .dto import PropiedadDB
from .mapeadores import MapeadorPropiedadDB
from uuid import UUID


class FabricaPropiedadesDB(Fabrica):
    def crear_objeto(self, obj, mapeador: Mapeador | None = None) -> Propiedad:
        mapeador = mapeador or MapeadorPropiedadDB()
        result = mapeador.dto_a_entidad(obj)
        assert isinstance(result, Propiedad)
        return result


logger = logger.getChild("repo-propiedades")


class RepositorioPropiedadesDB(RepositorioPropiedades):
    def __init__(self):
        self._fabrica_propiedades: FabricaPropiedadesDB = FabricaPropiedadesDB()

    @property
    def fabrica_propiedades(self):
        return self._fabrica_propiedades

    def obtener_por_id(self, id: UUID) -> Propiedad | None:
        logger.info(f"Obtaining model with id {id}")
        db_model = db_session.query(PropiedadDB).filter_by(id=str(id)).one_or_none()
        if db_model is None:
            return None
        return self.fabrica_propiedades.crear_objeto(db_model)

    def obtener_todos(self) -> list[Propiedad]:
        logger.info("Obtaining all models")
        propiedades = db_session.query(PropiedadDB).all()
        return [
            self.fabrica_propiedades.crear_objeto(propiedad)
            for propiedad in propiedades
        ]

    def agregar(self, entity: Propiedad):
        db_model = MapeadorPropiedadDB().entidad_a_dto(entity)
        logger.info(f"Adding model with id {db_model.id}")
        db_session.add(db_model)

    def actualizar(self, entity: Propiedad):
        logger.info(f"Updating model with id {entity.id}")
        db_model = MapeadorPropiedadDB().entidad_a_dto(entity)
        db_session.merge(db_model)

    def eliminar(self, entity_id: UUID):
        logger.info(f"Deleting model with id {entity_id}")
        db_session.query(PropiedadDB).filter_by(id=str(entity_id)).delete()

    def obtener_por_columna(self, columna: str, valor: str) -> list[Propiedad]:
        propiedades = (
            db_session.query(PropiedadDB)
            .where(text(f"{columna} = :valor"))
            .params(valor=valor)
        ).all()
        return [
            self.fabrica_propiedades.crear_objeto(propiedad)
            for propiedad in propiedades
        ]
