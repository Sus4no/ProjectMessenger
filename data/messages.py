import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
import datetime

class Messages(SqlAlchemyBase, UserMixin):
    __tablename__ = 'messages'
    mes_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    sender = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    receiver = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    def get_id(self):
        return self.user_id
