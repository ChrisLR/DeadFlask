import logging
from contextlib import contextmanager
from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from deadflask.server.app import app

_logger = logging.getLogger()

Base = declarative_base()


def connect_db(db_config):
    username = db_config["username"]
    password = db_config["password"]
    host = db_config["host"]
    dbname = db_config["dbname"]
    connection_string = f"postgres+psycopg2://{username}:{password}@{host}/{dbname}"

    Session = sessionmaker()
    engine = create_engine(connection_string, echo=True)
    metadata = Base.metadata
    metadata.create_all(engine)

    conn = engine.connect()
    session = Session(bind=conn)

    return session


def get_session_maker(db_config):
    username = db_config["username"]
    password = db_config["password"]
    host = db_config["host"]
    dbname = db_config["dbname"]
    connection_string = f"postgres+psycopg2://{username}:{password}@{host}/{dbname}"

    engine = create_engine(connection_string, echo=True)
    metadata = Base.metadata
    metadata.create_all(engine)
    session_maker = sessionmaker(engine)

    return session_maker


def with_session(func):
    """
    Decorator for session_scope
    """
    @wraps(func)
    def _wrapped_func(*args, **kwargs):
        with session_scope() as session:
            return func(*args, **kwargs, session=session)

    return _wrapped_func


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = app.session_maker()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def prepare_new_session():
    new_session = app.session_maker()
    app.db_session = new_session


def commit_session(response):
    app.db_session.commit()

    return response
