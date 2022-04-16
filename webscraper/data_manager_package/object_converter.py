from .sqlalchemy_classes import StoreChain, Store, StoreLocation, ProductCategory, Product, StoreProduct

class DatabaseObjectConverter:
    
    @staticmethod
    def convert_to_database(database_payload):
        return database_payload

    @staticmethod
    def convert_to_item(database_object):
        return database_object
