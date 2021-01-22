from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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
