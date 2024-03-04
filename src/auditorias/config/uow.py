""" from auditorias.config.db import db_session
from auditorias.seedwork.infraestructura.uow import UnidadTrabajo, Batch


class UnidadTrabajoSQLAlchemy(UnidadTrabajo):
    def _limpiar_batches(self):
        self.batches = []

    def savepoints(self) -> list:
        return list(db_session.get_nested_transaction())

    def commit(self):
        for batch in self.batches:
            batch.run()

        db_session.commit()
        super().commit()

    def rollback(self, savepoint=None):
        if savepoint:
            savepoint.rollback()
        else:
            db_session.rollback()
        super().rollback()

    def savepoint(self):
        db_session.begin_nested()
 """