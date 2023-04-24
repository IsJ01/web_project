import sqlalchemy
from flask_login import UserMixin
from data.db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


# класс пользователя.
class User(SqlAlchemyBase, UserMixin):
    # имя таблицы
    __tablename__ = 'users'
    # id пользователя.
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    # имя
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # фамилия
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # почта
    email = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    # пароль.
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # метод, задающий пароль.
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    # метод, проверяющий корректность пароля.
    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)