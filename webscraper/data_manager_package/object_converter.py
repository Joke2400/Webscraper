from .sqlalchemy_classes import StoreChain, Store, StoreLocation, ProductCategory, Product, StoreProduct

class DatabaseObjectConverter:
    
    @staticmethod
    def convert_store_to_database(session, payload):
        store = None
        exists = True if len(session.query(Store).filter_by(name=payload["name"]).all()) > 0 else False
        if not exists:
            chain = session.query(StoreChain).filter_by(name=payload["chain"]).all()[0]
            store = Store(
            chain=chain,
            name=payload["name"],
            open_times=payload["open_times"],
            date_added=None,
            date_updated=None,
            select=payload["select"]
            )
        return store

    @staticmethod
    def convert_location_to_database(store, payload):
        location = StoreLocation(
            store=store,
            formatted_address=payload["address"],
            lat=None,
            lon=None,
            maps_place_id=None,
            maps_plus_code=None
        )
        return location

    @staticmethod
    def convert_product_to_database(session, payload):
        product = None
        exists = True if len(session.query(Product).filter_by(name=payload["name"]).all()) > 0 else False
        product = Product(
            name=payload["name"],
            subname=payload["subname"],
            quantity=payload["quantity"],
            unit=payload["unit"],
            img=payload["img"]  
            )
        product.ean = payload["ean"]
        return product, exists

    @staticmethod
    def convert_store_product_to_database(session, payload):
        store = session.query(Store).filter_by(name=payload["store_name"].lower()).all()[0]
        store_product = StoreProduct(
            store=store,
            store_id = store.id,
            price=payload["price"],
            unit_price=payload["unit_price"],
            shelf_name=payload["shelf_name"],
            shelf_href=payload["shelf_href"]
        )
        return store, store_product