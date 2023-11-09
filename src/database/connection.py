from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config
#from urllib.parse import quote  #if use other db

from .tables import Base
from .tables import Attendant, Solicitation

class DatabaseManager:
    def __init__(self):
        self.engine = self.__create_engine_instance()
        self.session = None
    

    def __create_engine_instance(self):
        try:
            #To use other db, for example postgres
            """db_config = {
                'database': config('DB_NAME'),
                'user': config('DB_USER'),
                'password': config('DB_PASSWORD'),
                'host': config('DB_HOST'),
                'port': config('DB_PORT')      
            }
            db_url = f"postgresql://{db_config['user']}:{encoded_password}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
            encoded_password = quote(db_config['password'])"""

            db_url = config('DB_PATH', default='sqlite:///costomer_service.db')
            engine = create_engine(db_url)
            return engine
        except Exception as e:
            print(f"Error creating database engine: {e}")
            return None


    def open_session(self):
        try:
            if self.session is None:
                Session = sessionmaker(bind=self.engine)
                self.session = Session()
            return self.session
        except Exception as e:
            print(f"Error opening session: {e}")
            return None


    def close_session(self):
        try:
            if self.session is not None:
                self.session.close()
                self.session = None
        except Exception as e:
            print(f"Error closing session: {e}")


    def create_tables(self):
        """
        This function creates tables if they don't exist.
        """
        try:
            Base.metadata.create_all(self.engine)
            print("Tables created successfully.")
        except Exception as e:
            print(f"Error creating tables: {e}")
