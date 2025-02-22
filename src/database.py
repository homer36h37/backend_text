from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# подключение к базе данных
SQLALCHEMY_DATABASE_URL = ""
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# создаем таблицы
Base.metadata.create_all(bind=engine)
 
# создаем сессию подключения к бд
SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()