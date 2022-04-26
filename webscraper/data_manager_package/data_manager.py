import os
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

    def _object_already_exists(self, target, **kwargs): # <-- Needs improving
        name = kwargs.get("name", False)
        if name is not False:
            with self.session.no_autoflush:
                db = self.session.query(target).filter_by(name=name).all()
            if len(db) > 0:
                name = True

        ean = kwargs.get("ean", False)
        if ean is not False:
            with self.session.no_autoflush:
                db = self.session.query(target).filter_by(ean=ean).all()
            if len(db) > 0:
                ean = True

        if name is True or ean is True:
            return True
        return False
        
    def db_insert(self, obj=None, commit=False):
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
        if not self._object_already_exists(
            target=Store, name=payload["name"]):
            chain = self.session.query(StoreChain)\
                .filter_by(name=payload["chain"]).all()[0]
            store = self.create_store(chain_obj=chain, **payload)
            
            if self.db_insert(obj=store):
                location = self.create_location(store_obj=store, **payload)                
                if not self.db_insert(obj=location, commit=True):
                    raise NotImplementedError(
                        "[add_store]: Store location could not be added into database.")
            else:
                raise NotImplementedError(
                    "[add_store]: Store could not be added into database.")
        else:
            print(f"Store: {payload['name'].title()} is already in database.")
        
    def add_product(self, **payload):
        store = self.session.query(Store)\
            .filter_by(name=payload["store_name"].lower()).all()[0]
        if not self._object_already_exists(
            target=Product, ean=payload["ean"]):
            product = self.create_product(**payload)
            if self.db_insert(obj=product):
                store_product = self.create_store_product(store_obj=store, **payload)
                try:
                    store_product.product = product
                    store.products.append(store_product)

                except SQLAlchemyError:
                    raise NotImplementedError("[add_product]: Store product could not be added into database.")
            else:
                raise NotImplementedError("[add_product]: Product could not be added into database.")
        else:
            print(f"Product: {payload['name'].title()} is already in database.")
            product = self.session.query(Product).filter_by(ean=payload["ean"]).all()[0]
            query = self.session.query(StoreProduct).filter_by(store_id=store.id, product_ean=payload["ean"]).all()
            if len(query) == 0:
                store_product = self.create_store_product(store_obj=store, **payload)
                try:
                    store_product.product = product
                    store.products.append(store_product)
                except SQLAlchemyError:
                    raise NotImplementedError("[add_product]: Store product could not be added into database.")
        
    def create_store(self, chain_obj, **kwargs):
        store = Store(
            chain=chain_obj,
            name=kwargs["name"],
            open_times=kwargs["open_times"],
            date_added=None,
            date_updated=None,
            select=kwargs["select"])
        return store

    def create_location(self, store_obj, **kwargs):
        location = StoreLocation(
            store=store_obj,
            formatted_address=kwargs["address"],
            lat=None,
            lon=None,
            maps_place_id=None,
            maps_plus_code=None)
        return location

    def create_product(self, **kwargs):
        product = Product(
            name=kwargs["name"],
            subname=kwargs["subname"],
            quantity=kwargs["quantity"],
            unit=kwargs["unit"],
            img=kwargs["img"])
        product.ean = kwargs["ean"]
        return product

    def create_store_product(self, store_obj, **kwargs):
        store_product = StoreProduct(
            store=store_obj,
            store_id=store_obj.id,
            price=kwargs["price"],
            unit_price=kwargs["unit_price"],
            shelf_name=kwargs["shelf_name"],
            shelf_href=kwargs["shelf_href"])
        return store_product
