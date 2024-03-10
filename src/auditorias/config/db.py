import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

database_uri = os.environ.get("SQLALCHEMY_DATABASE_URI")
if not database_uri:
    database_uri = "mysql+mysqldb://root:root@127.0.0.1:3306/contratos"

engine = create_engine(
    database_uri, execution_options={"isolation_level": "READ COMMITTED"}
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
    import auditorias.modulos.verificacion.infraestructura.dto as auditorias_dto

    Base.metadata.create_all(bind=engine)
