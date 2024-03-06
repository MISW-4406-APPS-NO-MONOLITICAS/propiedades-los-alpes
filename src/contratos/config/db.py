from flask import Flask
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

databse_uri = os.environ.get("SQLALCHEMY_DATABASE_URI")
if not databse_uri:
    databse_uri = "mysql+mysqldb://root:root@database/contratos"

engine = create_engine(
    databse_uri, execution_options={"isolation_level": "READ COMMITTED"}
)
db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
)
Base = declarative_base()


# Init db with mysql
def init_db():
    import contratos.modulos.contratos.infraestructura.dto as contratos_dto

    Base.metadata.create_all(bind=engine)
