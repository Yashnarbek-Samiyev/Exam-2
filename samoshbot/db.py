from pyparsing import C
from sqlalchemy.orm import sessionmaker
import enum
import datetime
from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db
engine = db.create_engine(
    'postgresql+psycopg2://postgres:1223@localhost:5432/samplov')
meta = MetaData()
Base = declarative_base()


class CategoryTable(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)

    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now,
                        onupdate=datetime.datetime.now)


class ProductTable(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(Integer, ForeignKey('category.id'))
    title = Column(String)
    price = Column(Integer)

    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now,
                        onupdate=datetime.datetime.now)


def get_category_all():
    Session = sessionmaker(bind=engine)
    session = Session()

    result = session.query(CategoryTable).all()
    return result if result else None


def get_category_id_by_name(name):
    Session = sessionmaker(bind=engine)
    session = Session()

    result = session.query(CategoryTable).filter(
        CategoryTable.title == name).first()
    return result if result else None


def get_category_product(category_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    result = session.query(ProductTable).filter(
        ProductTable.category == category_id).all()
    return result if result else None
