from sqlalchemy import create_engine, Column, String, Integer, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import sys
import time
from datetime import date, timedelta

engine = create_engine("mysql://root:cake@localhost/food_storage")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Item_name(Base):
    """Class for initializing item name for SQL.

    Arguments:
        Base {declarative base} -- Construct a base class for declarative class definitions.
    """


    __tablename__ = "item_name"

    ingredient = Column(String, primary_key=True)

    def __init__(self, ingredient):
        """initialiser function for correct setup of item name for SQL

        Arguments:
            ingredient {string} name of the ingredient
        """
        self.ingredient = ingredient

class Item(Base):
    """Class for initializing items for SQL and holds all functions for interactions with items

    Arguments:
        Base {declarative base} -- Construct a base class for declarative class definitions

    """
#

    __tablename__ = "item"

    EAN = Column(Integer, primary_key=True)
    ingredient = Column(String)
    default_amount = Column(Integer)

    def __init__(self, EAN, ingredient, default_amount):
        """initialiser function for correct setup of items for SQL

        Arguments:
            EAN {integer} -- [description]
            ingredient {string} -- [description]
            default_amount {integer} -- [description]
        """
        self.EAN = EAN
        self.ingredient = ingredient
        self.default_amount = default_amount

    def new_store(ingredient, default_amount, EAN):
        """Function for adding new items in the item_name and items table in the database
        Includes check function if the name of item already exists

        Arguments:
            ingredient {string} -- name of the ingredient/item
            default_amount {integer} -- the default amount of an item
            EAN {integer} -- European aricle number
        """
        check = session.query(Item_name).get(ingredient)
        try:
            if check.ingredient == ingredient:
                pass
        except AttributeError:
            new_item = Item_name(ingredient)
            session.add(new_item)
            session.commit()
        new_item = Item(EAN, ingredient, default_amount)
        session.add(new_item)
        session.commit()
        
        

    def store(storage, EAN, expiredate):
        """Function to filter what storage an item is going to get stored into with check if the item exists in the database

        Arguments:
            storage {sting} -- describes which storage to store into
            EAN {integer} -- European article number for check if the item excist in the database
            expiredate {date} -- information on when the item/ingredient expires
            
        Returns:
            if 'no_item':
                string -- Tells the program that this item ha no information in the database
            else:
                Dictionary -- Tells the system information on all of the same items stored in the storage used
        """
        try:
            check = session.query(Item).get(EAN)
            if check.EAN == EAN:
                if storage == 'dry':
                    Dry_store.store(EAN, expiredate, check.default_amount)
                    return session.query(Dry_store).filter(Dry_store.EAN == EAN).all()
                elif storage == 'fridge':
                    Fridge_store.store(EAN, expiredate, check.default_amount)
                    return session.query(Fridge_store).filter(Fridge_store.EAN == EAN).all()
                elif storage == 'freezer':
                    Freezer_store.store(EAN, expiredate, check.default_amount)
                    return session.query(Freezer_store).filter(Freezer_store.EAN == EAN).all()
        except AttributeError:
            return 'no_item'


    def use(EAN, amount, storage):
        """Function for updating the amount of a spesific item.

        Arguments:
            EAN {integer} -- tells the system the filter for the spesific item/ingredient
            amount {integer} -- tells the system how much of the spesific item used
            storage {string} -- tells the system what storage you are using from

        Returns:
            tuple -- index 0 tells the system if usage is higher then stored 
                     index1 tells the system the amount stored
        """
        if storage == 'dry':
            storage_use = Dry_store
        elif storage == 'fridge':
            storage_use = Fridge_store
        elif storage == 'freezer':
            storage_use = Freezer_store
        item = storage_use.get_bydate(EAN)
        stored = 0
        for i in item:
            stored += i.amount
        if stored < amount:
            return "to-much", stored
        else:
            for i in item:
                if amount == 0:
                    break
                elif i.amount < amount:
                    amount -= i.amount
                    storage_use.delete(i.id)
                elif i.amount > amount:
                    update = i.amount - amount
                    amount = 0
                    storage_use.update(i.id, update)
            return 'ok', stored
                        
    def delete(storage, id):
        """Function for filtering where an item is deleted from.

        Arguments:
            storage {String} -- Tells the system what storage to delete from
            id {integer} -- Tells the system the spesific item id to delete
        """
        if storage == 'freezer':
            Freezer_store.delete(id)
        elif storage == 'fridge':
            Fridge_store.delete(id)
        elif storage == 'dry':
            Dry_store.delete(id)

    def del_conf(storage, id):
        if storage == 'freezer':
            return session.query(Freezer_store).get(id)
        elif storage == 'fridge':
            return session.query(Fridge_store).get(id)
        elif storage == 'dry':
            return session.query(Dry_store).get(id)



    def get():
        """Function for querrying all items within the item table

        Returns:
            dictionary -- Returns all information in the table
        """
        return session.query(Item).all()

    def get_EAN(EAN):
        """function to get the information of a spesific item

        Arguments:
            EAN {integer} -- item identification

        Returns:
            dictionary -- returns informaion on a spesific item
        """
        return session.query(Item).filter(Item.EAN == EAN).all()

    def webcheck():
        """function for getting all items stored with 10 days or less to expiredate

        Returns:
            dictionary -- returns infroamtion on all items stored with 10 days or less to expiredate
        """
        timeframe = date.today() + timedelta(days=10)
        freezer = session.query(Freezer_store).filter(Freezer_store.expiredate <= timeframe).all()
        dry = session.query(Dry_store).filter(Dry_store.expiredate <= timeframe).all()
        fridge = session.query(Fridge_store).filter(Fridge_store.expiredate <= timeframe).all()
        return freezer + dry + fridge

    def search(search):
        """function for searching for items by using name

        Arguments:
            search {string} -- name of the item/ingredient

        Returns:
            tuple -- returns information from all storages with the name one are searching for
        """
        item = session.query(Item).filter(Item.ingredient == search).all()
        freezer = []
        dry = []
        fridge = []
        for i in item:
            freezer.append(session.query(Freezer_store).filter(Freezer_store.EAN == i.EAN).all())
            dry.append(session.query(Dry_store).filter(Dry_store.EAN == i.EAN).all())
            fridge.append(session.query(Fridge_store).filter(Fridge_store.EAN == i.EAN).all())
                        
        return freezer, dry, fridge


class Dry_store(Base):
    """Class for initializing items for SQL and holds all functions for interactions with the storage

    Arguments:
        Base {declarative base} -- Construct a base class for declarative class definitions
    """

    __tablename__ = "dry_storage"

    id = Column(Integer, primary_key=True)
    EAN = Column(Integer)
    amount = Column(Integer)
    expiredate = Column(DateTime)

    def __init__(self, EAN, amount, expiredate):
        """initialiser function for correct setup of items for SQL

        Arguments:
            EAN {integer} --  tells the system the what type of item/ingredient this is
            amount {integer} -- How much is left of the item/ingredient
            expiredate {date} -- Expiration date
        """
        self.EAN = EAN
        self.amount = amount
        self.expiredate = expiredate

    def get():
        """Function to get all information in the dry_storage table

        Returns:
            dictionary -- all information in the dry_storage table
        """
        return session.query(Dry_store).all()

    def get_bydate(EAN):
        """Function for getting spesific item by EAN sorted by date

        Returns:
            dictionaty -- all information on a spesific item sorted by date
        """

        return session.query(Dry_store).filter(Dry_store.EAN == EAN).order_by(Dry_store.expiredate).all()


    def store(EAN, expiredate, quantity):
        """Function to store new items/ingredients in the dry storage

        Arguments:
            EAN {integer} -- tells the system the what type of item/ingredient this is
            expiredate {date} -- Expiration date
            quantity {integer} -- Quantity of the item stored
        """
        new_item = Dry_store(EAN, quantity, expiredate)
        session.add(new_item)
        session.commit()
        session.close()

    def update(id, amount):
        """Update function for anything in the dry storage

        Arguments:
            id {integer} -- Unique id for an item
            amount {integer} -- new amount left for the item
        """
        session.query(Dry_store).filter(Dry_store.id == id).update({"amount": amount})
        session.commit()

    def delete(id):
        """Function for deleting an item in the dry storage

        Arguments:
            id {integer} -- Unique id for an item
        """
        session.query(Dry_store).filter(Dry_store.id == id).delete()
        session.commit()


class Freezer_store(Base):
    """Class for initializing items for SQL and holds all functions for interactions with the storage

    Arguments:
        Base {declarative base} -- Construct a base class for declarative class definitions
    """

    __tablename__ = "freezer_storage"

    id = Column(Integer, primary_key=True)
    EAN = Column(Integer)
    amount = Column(Integer)
    expiredate = Column(DateTime)

    def __init__(self, EAN, amount, expiredate):
        """initialiser function for correct setup of items for SQL

        Arguments:
            EAN {integer} --  tells the system the what type of item/ingredient this is
            amount {integer} -- How much is left of the item/ingredient
            expiredate {date} -- Expiration date
        """
        self.EAN = EAN
        self.amount = amount
        self.expiredate = expiredate

    def get():
        """Function to get all information in the freezer_storage table

        Returns:
            dictionary -- all information in the freezer_storage table
        """    
        return session.query(Freezer_store).all()

    def get_bydate(EAN):
        """Function for getting spesific item by EAN sorted by date

        Returns:
            dictionaty -- all information on a spesific item sorted by date
        """

        return session.query(Freezer_store).filter(Freezer_store.EAN == EAN).order_by(Freezer_store.expiredate).all()

    def store(EAN, expiredate, quantity):
        """Function to store new items/ingredients in the freezer

        Arguments:
            EAN {integer} -- tells the system the what type of item/ingredient this is
            expiredate {date} -- Expiration date
            quantity {integer} -- Quantity of the item stored
        """
        new_item = Freezer_store(EAN, quantity, expiredate)
        session.add(new_item)
        session.commit()
        session.close()


    def update(id, amount):
        """Update function for anything in the freezer

        Arguments:
            id {integer} -- Unique id for an item
            amount {integer} -- new amount left for the item
        """
        session.query(Freezer_store).filter(Freezer_store.id == id).update({"amount": amount})
        session.commit()

    
    def delete(id):
        """Function for deleting an item in the freezer

        Arguments:
            id {integer} -- Unique id for an item
        """
        session.query(Freezer_store).filter(Freezer_store.id == id).delete()
        session.commit()

class Fridge_store(Base):
    """Class for initializing items for SQL and holds all functions for interactions with the storage

    Arguments:
        Base {declarative base} -- Construct a base class for declarative class definitions
    """

    __tablename__ = "fridge_storage"

    id = Column(Integer, primary_key=True)
    EAN = Column(Integer)
    amount = Column(Integer)
    expiredate = Column(DateTime)

    def __init__(self, EAN, amount, expiredate):
        """initialiser function for correct setup of items for SQL

        Arguments:
            EAN {integer} --  tells the system the what type of item/ingredient this is
            amount {integer} -- How much is left of the item/ingredient
            expiredate {date} -- Expiration date
        """
        self.EAN = EAN
        self.amount = amount
        self.expiredate = expiredate

    def get():
        """Function to get all information in the fridge_storage table

        Returns:
            dictionary -- all information in the fridge_storage table
        """    
        return session.query(Fridge_store).all()

    def get_bydate(EAN):
        """Function for getting spesific item by EAN sorted by date

        Returns:
            dictionaty -- all information on a spesific item sorted by date
        """

        return session.query(Fridge_store).filter(Fridge_store.EAN == EAN).order_by(Fridge_store.expiredate).all()

    def store(EAN, expiredate, quantity):
        """Function to store new items/ingredients in the fridge

        Arguments:
            EAN {integer} -- tells the system the what type of item/ingredient this is
            expiredate {date} -- Expiration date
            quantity {integer} -- Quantity of the item stored
        """
        new_item = Fridge_store(EAN, quantity, expiredate)
        session.add(new_item)
        session.commit()
        session.close()

    def update(id, amount):
        """Update function for anything in the fridge

        Arguments:
            id {integer} -- Unique id for an item
            amount {integer} -- new amount left for the item
        """
        session.query(Fridge_store).filter(Fridge_store.id == id).update({"amount": amount})
        session.commit()



    def delete(id):
        """Function for deleting an item in the fridge

        Arguments:
            id {integer} -- Unique id for an item
        """
        session.query(Fridge_store).filter(Fridge_store.id == id).delete()
        session.commit()

    
