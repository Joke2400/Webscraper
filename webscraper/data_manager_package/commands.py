from abc import ABC, abstractmethod
from webscraper.data_manager_package.sqlalchemy_classes import StoreChain, Store, StoreLocation, Product, StoreProduct

class Command(ABC):

    def __init__(self, receiver, payload):
        self.receiver = receiver
        self.payload = payload

    @abstractmethod
    def execute(self):
        pass

class DBStoreChainRequest(Command):

    def execute(self):
        def query_func(session):
            result = session.query(StoreChain).filter_by(**self.payload).all()
            return result

        result = self.receiver.fetch_request(query_func)
        return result

class DBStoreRequest(Command):

    def execute(self):
        def query_func(session):
            result = session.query(Store).filter_by(**self.payload).all()
            return result

        result = self.receiver.fetch_request(query_func)
        return result

class DBStoreProductRequest(Command):

    def execute(self):
        def query_func(session):
            result = session.query(StoreProduct).filter_by(**self.payload).all()
            return result

        result = self.receiver.fetch_request(query_func)
        return result

class DBAddStore(Command):

    def execute(self):
        self.receiver.add_store(**self.payload)

class DBAddProduct(Command):

    def execute(self):
        self.receiver.add_product(**self.payload)