import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from webscraper.data.filepaths import FilePaths
from .sqlalchemy_classes import Base, DatabaseInitializer
from .object_converter import DatabaseObjectConverter

class DataManager:
    
    def __init__(self):
        self.session = None
        self.object_converter = DatabaseObjectConverter()
        self.database_engine = create_engine(f"sqlite:///{FilePaths.database_path}", echo=False)
        Base.metadata.create_all(bind=self.database_engine)

    def get_session(self):
        if self.session is not None:
            return self.session
        return None

    def start_session(self):
        print("Database session started.")
        self.sessionmaker = sessionmaker(bind=self.database_engine)
        self.session = self.sessionmaker()
        self.initializer = DatabaseInitializer(self.session)

    def close_session(self):
        print("Database session ended.")
        self.session.close()

    def reset_database(self):
        print("Removing and resetting database because reset_database() method was called...")
        if self.session is not None:
            self.session.close()
        removed = False
        try:
            os.remove(FilePaths.database_path)
            removed = True
        except FileNotFoundError:
            print("Error when removing database, database file missing...")
        try:
            if removed:
                self.database_engine = create_engine(f"sqlite:///{FilePaths.database_path}", echo=False)
                Base.metadata.create_all(bind=self.database_engine)
                print(f"Created new database at: {FilePaths.database_path}")
        except Exception("Error creating database file"):
            self.database_engine = None

    def fetch_request(self, func):
        result = func(self.session)
        return result
        
    def insert_into(self, payload):
        obj = self.object_converter.convert_to_database(payload) #Either Store, Product or StoreLocation
        self.session.add(obj)
        self.session.commit()

'''
Data Manager

* Event driven pattern
* Initially synchronous, later maybe async

        Data management ->
            Asking Data manager for store data
            Sending store and product data Data manager



Data manager ->
    Standalone manager for database queries and commits
    Receiving and sending data to spider

    Centralised storage for all store/product/location data

    ALL DATA FLOWS THROUGH THIS NEW CLASS AT LEAST ONCE BEFORE
    ITS DISPLAYED TO THE USER

'''