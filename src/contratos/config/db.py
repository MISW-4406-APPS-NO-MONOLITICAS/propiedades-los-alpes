from flask import Flask
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

databse_uri = os.environ.get("SQLALCHEMY_DATABASE_URI")
if not databse_uri:
    databse_uri = "mysql+mysqldb://root:root@database/contratos"


def create_db_engine():
    return create_engine(
        databse_uri, execution_options={"isolation_level": "READ COMMITTED"}
    )


def create_db_session():
    return scoped_session(
        sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=create_db_engine(),
        )
    )


db_session = create_db_session()

Base = declarative_base()


# Init db with mysql
def init_db():
    import contratos.modulos.contratos.infraestructura.dto as contratos_dto
    import contratos.modulos.sagas.db_models as sagas_dto

    Base.metadata.create_all(bind=create_db_engine())
