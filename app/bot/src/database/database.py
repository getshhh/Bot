from sqlalchemy import create_engine, Column, Integer, String, Text, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.settings import POSTGRESQL_URI

# Создаем базовый класс для объявления моделей
Base = declarative_base()


# Определяем модель таблицы easy_tasks_three
class EasyTasksThree(Base):
    __tablename__ = 'easy_tasks_three'
    id = Column(BigInteger, primary_key=True)
    deadline = Column(Text)
    task_text = Column(Text)
    coins_amount = Column(Integer)
    owner = Column(String)
    media = Column(String)


# Определяем модель таблицы easy_tasks_two
class EasyTasksTwo(Base):
    __tablename__ = 'easy_tasks_two'
    id = Column(BigInteger, primary_key=True)
    deadline = Column(Text)
    task_text = Column(Text)
    coins_amount = Column(Integer)
    owner = Column(String)
    media = Column(String)


# Определяем модель таблицы easy_tasks
class EasyTasks(Base):
    __tablename__ = 'easy_tasks'
    id = Column(BigInteger, primary_key=True)
    deadline = Column(Text)
    task_text = Column(Text)
    coins_amount = Column(Integer)
    owner = Column(String)
    media = Column(String)


# Определяем модель таблицы wow_tasks
class WowTasks(Base):
    __tablename__ = 'wow_tasks'
    id = Column(BigInteger, primary_key=True)
    deadline = Column(Text)
    task_text = Column(Text)
    coins_amount = Column(Integer)
    owner = Column(String)
    media = Column(String)


# Определяем модель таблицы user_access
class UserAccess(Base):
    __tablename__ = 'user_access'
    id = Column(BigInteger, primary_key=True)
    access = Column(String)


# Определяем модель таблицы users
class Users(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    balance = Column(Integer)
    link = Column(String)
    role = Column(String)


# Создаем соединение к базе данных
engine = create_engine(POSTGRESQL_URI, pool_size=10, max_overflow=20, echo=True, pool_recycle=3600)

# Создаем таблицы, если их нет
Base.metadata.create_all(engine)

# Создаем сессию
Session = sessionmaker(bind=engine)
session = Session()
