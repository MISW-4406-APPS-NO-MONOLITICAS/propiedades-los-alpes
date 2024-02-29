from listados.config.db import db
from listados.seedwork.infraestructura.uow import UnidadTrabajo, Batch


class UnidadTrabajoSQLAlchemy(UnidadTrabajo):
    def savepoints(self) -> list:
        return list(db.session.get_nested_transaction())

    def commit(self):
        for batch in self.batches:
            batch.operacion(*batch.args, **batch.kwargs)

        db.session.commit()
        super().commit()

    def rollback(self, savepoint=None):
        if savepoint:
            savepoint.rollback()
        else:
            db.session.rollback()
        super().rollback()

    def savepoint(self):
        db.session.begin_nested()
