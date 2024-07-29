from sqlalchemy.orm import declarative_base, DeclarativeMeta, sessionmaker, scoped_session, Session
from sqlalchemy import create_engine


SqlAlchemyBase: DeclarativeMeta = declarative_base()

__factory = None


def global_init():
    global __factory

    conn_str = f'sqlite:///app/database/db/blog.db?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = create_engine(conn_str, echo=False)
    __factory = sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()

