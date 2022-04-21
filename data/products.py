import datetime

import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Object(SqlAlchemyBase):
    __tablename__ = 'Products'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    place = sqlalchemy.Column(sqlalchemy.String)
    category = sqlalchemy.Column(sqlalchemy.String)
    type = sqlalchemy.Column(sqlalchemy.String)
    in_UNESCO = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    # leader = orm.relation('User')
    """categories = orm.relation("Category",
                              secondary="association",
                              backref="jobs")"""
