import datetime

import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Object(SqlAlchemyBase):
    __tablename__ = 'Products'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    address_text = sqlalchemy.Column(sqlalchemy.String)
    category = sqlalchemy.Column(sqlalchemy.String)
    map_pos = sqlalchemy.Column(sqlalchemy.String)
    object_type = sqlalchemy.Column(sqlalchemy.String)
    info = sqlalchemy.Column(sqlalchemy.String)
    photo = sqlalchemy.Column(sqlalchemy.String)
    unesco_status = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    # leader = orm.relation('User')
    """categories = orm.relation("Category",
                              secondary="association",
                              backref="jobs")"""
