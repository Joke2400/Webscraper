import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .sqlalchemy_classes import Product

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
        if self.session is None:
            self.sessionmaker = sessionmaker(bind=self.database_engine)
            self.session = self.sessionmaker()
            print("\n[Database session started]\n")

    def close_session(self):
        self.session.close()
        print("\n[Database session ended]\n")

    def reset_database(self):
        print("\nRemoving and resetting database because reset_database() method was called...")
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
                #Initializer will be removed in final version
                self.start_session()
                self.initializer = DatabaseInitializer(self.session)       

        except:
            print("Error creating database file")
            self.database_engine = None

    def fetch_request(self, func):
        result = func(self.session)
        return result
        
    def add_store(self, **payload):
        store = self.object_converter.convert_store_to_database(session=self.session, payload=payload)
        if store is not None:
            self.session.add(store)
            location = self.object_converter.convert_location_to_database(store=store, payload=payload)
            self.session.add(location)
            self.session.commit()

    def add_product(self, **payload):
        product, exists = self.object_converter.convert_product_to_database(session=self.session, payload=payload)
        if exists:
            product = self.session.query(Product).filter_by(name=payload["name"]).all()[0]
            store, store_product = self.object_converter.convert_store_product_to_database(session=self.session, payload=payload)
            store_product.product = product
            store.products.append(store_product) 
            self.session.commit()
        else:
            store, store_product = self.object_converter.convert_store_product_to_database(session=self.session, payload=payload)
            store_product.product = product
            store.products.append(store_product) 
            self.session.commit()

        