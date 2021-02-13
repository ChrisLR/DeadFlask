import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

_logger = logging.getLogger()

Base = declarative_base()


class DBConnection(object):
    def __init__(self, db_config):
        self.username = db_config["username"]
        self.password = db_config["password"]
        self.host = db_config["host"]
        self.dbname = db_config["dbname"]
        self.connection_string = f"postgres+psycopg2://{self.username}:{self.password}@{self.host}/{self.dbname}"
        self.session = None
        self.engine = create_engine(self.connection_string, echo=True)

    def connect(self):
        _logger.info(f"Connecting to {self.connection_string}..")
        self.session = scoped_session(sessionmaker(self.engine))
        self.on_connect()

    def on_connect(self):
        _logger.info(f"Creating metadata..")
        metadata = Base.metadata
        metadata.create_all(self.engine)

    @property
    def query(self):
        if not self.session:
            self.connect()

        return self.session.query

    def prepare_new_session(self):
        _logger.info(f"Preparing new db session..")
        self.session()

    def commit_session(self, response):
        _logger.info(f"Committing db session..")
        self.session.commit()
        self.session.remove()

        return response

    def close(self):
        _logger.info(f"Closing db connection..")
        self.session.close()
