from .sqlalchemy_classes import StoreChain, Store, StoreLocation, ProductCategory, Product, StoreProduct

class DatabaseObjectConverter():
    
    @staticmethod
    def convert_to_database(database_object):
        return database_object

    @staticmethod
    def convert_to_item(database_object):
        return database_object
