from contratos.config.db import Session
from contratos.seedwork.infraestructura.uow import UnidadTrabajo, Batch


class UnidadTrabajoSQLAlchemy(UnidadTrabajo):
    def __init__(self):
        self.db_session = Session()

    def _limpiar_batches(self):
        self.batches = []

    def savepoints(self) -> list:
        return list(self.db_session.get_nested_transaction())

    def commit(self):
        for batch in self.batches:
            batch.run()

        self.db_session.commit()
        super().commit()

    def rollback(self, savepoint=None):
        if savepoint:
            savepoint.rollback()
        else:
            self.db_session.rollback()
        super().rollback()

    def savepoint(self):
        self.db_session.begin_nested()
