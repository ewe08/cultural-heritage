import datetime

import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Comment(SqlAlchemyBase):
    __tablename__ = 'Comments'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey("users.id"))
    post = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey("Products.id"))
    text = sqlalchemy.Column(sqlalchemy.String)
    leader = orm.relation('User')
    leader1 = orm.relation('Product')



