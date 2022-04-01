from sqlalchemy import Column,Integer,String,Numeric,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class StoreChain(Base):

    __tablename__ = "store_chains"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __init__(self, name):
        self.name = name

class Store(Base):

    __tablename__ = "stores"

    id = Column(Integer, primary_key=True)
    chain_id = Column(Integer, ForeignKey("store_chains.id"))
    name = Column(String, unique=True)
    open_times = Column(String)
    date_added = Column(String)
    date_updated = Column(String)
    select = Column(String)

    chain = relationship("StoreChain", backref="stores")
    products = relationship("StoreProduct", back_populates="store")

    def __init__(self, chain, name, open_times, date_added, date_updated, select):
        self.chain = chain
        self.name = name
        self.open_times = open_times
        self.date_added = date_added
        self.date_updated = date_updated
        self.select = select

class StoreLocation(Base):

    __tablename__ = "store_locations"

    id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey("stores.id"))
    formatted_address = Column(String, unique=True)
    lat = Column(String, unique=True)
    lon = Column(String, unique=True)
    maps_place_id = Column(String, unique=True)
    maps_plus_code = Column(String, unique=True)

    store = relationship("Store", backref=backref("location", uselist=False))

    def __init__(self, store, formatted_address, lat, lon, maps_place_id, maps_plus_code):
        self.store = store
        self.formatted_address = formatted_address
        self.lat = lat
        self.lon = lon
        self.maps_place_id = maps_place_id
        self.maps_plus_code = maps_plus_code

class ProductCategory(Base):

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

class Product(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    subname = Column(String)
    quantity = Column(String)
    unit = Column(String)

    stores = relationship("StoreProduct", back_populates="product")

    def __init__(self, name, subname, quantity, unit):
        self.name = name
        self.subname = subname
        self.quantity = quantity
        self.unit = unit

class StoreProduct(Base):

    __tablename__ = "store_products"

    store_id = Column(ForeignKey("stores.id"), primary_key=True)
    product_id = Column(ForeignKey("products.id"), primary_key=True)
    price = Column(Numeric)
    price_quantity = Column(String)
    shelf_name = Column(String)
    shelf_href = Column(String)

    store = relationship("Store", back_populates="products")
    product = relationship("Product", back_populates="stores")

class DatabaseInitializer:

    def __init__(self, session):
        self.session = session
        self.init_chains()


    def init_chains(self):
        chain_names = ["S-Market", "Prisma", "Sale", "Alepa", "ABC"]
        database = self.session.query(StoreChain).all()
        for chain in chain_names:
            found = False
            for item in database:
                if chain == item.name:
                    found = True
                    break
            if not found:
                self.session.add(StoreChain(chain))

        s_market = self.session.query(StoreChain).filter_by(name="S-Market").all()[0]
        s_market_grani = Store(
        chain=s_market,
        name="S-Market Grani",
        open_times="Avoinna T\u00e4n\u00e4\u00e4n: 07 - 22",
        date_added="05/10/2021 16:38:21",
        date_updated="04/03/2022 11:07:04",
        select="/store/select_store/6c6a1d4de1a6454f30a3a5c185e51c08",
        )
        self.session.add(s_market_grani)
        
        s_market_grani_location = StoreLocation(
        store=s_market_grani,
        formatted_address="Kauniaistentie 7, 02700 Kauniainen",
        lat="60.21018264713675",
        lon="24.72894144081173",
        maps_place_id="ChIJjSE14xP0jUYRa76Jrj659Nc",
        maps_plus_code="9GG66P6H+2C",
        )
        self.session.add(s_market_grani_location)


        maito_product = Product(
        name="Valio Luomu Rasvaton Maito 1 L",
        subname="valio luomu",
        quantity="1 l",
        unit="/kpl",
        )

        grani_product_1 = StoreProduct(
            price=0.98,
            price_quantity="0.98/l",
            shelf_name="hyllyväli 9",
            shelf_href="https://storemap.jupa.s-cloud.fi/indoor/v1/?apikey=u2fsdgvkx19gb2t7y60b9qjh4pr6bmbf7a8anb16tru%3d&s=643819774&f=1&hs=0370,0375,0380,0385,0390,0395&l=dep,sec2,zon",
        )
        grani_product_1.product = maito_product
        s_market_grani.products.append(grani_product_1)

        self.session.commit()
