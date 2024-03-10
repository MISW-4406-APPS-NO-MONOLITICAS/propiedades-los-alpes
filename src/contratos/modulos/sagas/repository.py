from contratos.config.db import Session
from contratos.modulos.sagas.db_models import SagaLogDB
from contratos.modulos.sagas.saga import SagaContratos
from contratos.seedwork.dominio.repositorios import Mapeador
from contratos.config.logger import logger

logger = logger.getChild("repo-saga-contratos")


class MapeadorSagaContratos(Mapeador):
    def entidad_a_dto(self, entidad: SagaContratos):
        assert isinstance(entidad, SagaContratos)
        return SagaLogDB(
            id_correlacion=entidad.id_correlacion,
            index=entidad.index,
            length=len(entidad.pasos()),
            estado=entidad.estado,
            last_event_processed=entidad.last_event_processed,
            last_command_dispatched=entidad.last_command_dispatched,
            fecha_creacion=entidad.fecha_creacion,
            fecha_actualizacion=entidad.fecha_actualizacion,
        )

    def dto_a_entidad(self, dto: SagaLogDB):
        return SagaContratos(
            id_correlacion=dto.id_correlacion,
            index=dto.index,
            estado=dto.estado,
            last_event_processed=dto.last_event_processed,
            last_command_dispatched=dto.last_command_dispatched,
            fecha_creacion=dto.fecha_creacion,
            fecha_actualizacion=dto.fecha_actualizacion,
        )


class RepositorioSagaContratosDB:
    def __init__(self):
        self._mapeador: MapeadorSagaContratos = MapeadorSagaContratos()
        self.db_session = Session()

    def obter_por_id(self, id_correlacion: str) -> SagaContratos:
        logger.info(f"Obtaining model {SagaLogDB.__name__} with id {id_correlacion}")
        return self._mapeador.dto_a_entidad(
            self.db_session.query(SagaLogDB).filter_by(id_correlacion=id_correlacion).one()
        )

    def obtener_por_id_or_none(self, id_correlacion: str) -> SagaContratos | None:
        logger.info(f"Obtaining model {SagaLogDB.__name__} with id {id_correlacion}")
        model = (
            self.db_session.query(SagaLogDB)
            .filter_by(id_correlacion=id_correlacion)
            .one_or_none()
        )
        if model:
            return self._mapeador.dto_a_entidad(model)
        return None

    def persistir(self, entity: SagaContratos):
        db_model = self._mapeador.entidad_a_dto(entity)
        # If the entity already exists, update it
        logger.info(
            f"Persisting {SagaLogDB.__name__} with id {entity.id_correlacion}"
        )
        self.db_session.merge(db_model)
        self.db_session.commit()
        logger.info(f"Commited changes to {SagaLogDB.__name__}")
