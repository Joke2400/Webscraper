import os
from telnetlib import SGA
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from .sqlalchemy_classes import StoreChain, Store, StoreLocation, ProductCategory, Product, StoreProduct

from webscraper.data.filepaths import FilePaths
from .sqlalchemy_classes import Base, DatabaseInitializer

class DataManager:
    
    def __init__(self):
        self.session = None
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

    def _object_already_exists(self, target, **kwargs):
        name = kwargs.get("name", False)
        if isinstance(name, str):
            name = True if len(self.session.query(target).filter_by(name=name).get()) > 0 else False
        ean = kwargs.get("ean", False)
        if isinstance(ean, str):
            ean = True if len(self.session.query(target).filter_by(ean=ean).get()) > 0 else False
        if name is True or ean is True:
            return True
        return False
        
    def db_insert(self, obj, commit=False):
        try:    
            self.session.add(obj)
            if commit:
                self.session.commit()
            return True
        except SQLAlchemyError:
            #print(str(e.orig))
            return False

    def db_remove(self):
        pass

    def add_store(self, **payload):
        if not self._object_already_exists(target=Store, name=payload["name"]):
            chain = self.session.query(StoreChain)\
                .filter_by(name=payload["chain"]).all()[0]
            store = Store(
                chain=chain,
                name=payload["name"],
                open_times=payload["open_times"],
                date_added=None,
                date_updated=None,
                select=payload["select"])

            if self.db_insert(obj=store):
                location = StoreLocation(
                    store=store,
                    formatted_address=payload["address"],
                    lat=None,
                    lon=None,
                    maps_place_id=None,
                    maps_plus_code=None)
                if not self.db_insert(obj=location, commit=True):
                    print("[add_store]: Store location could not be added into database.")
            else:
                print("[add_store]: Store could not be added into database.")
        else:
            raise NotImplementedError("[add_store]: Store object already present in database.")
        
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

        