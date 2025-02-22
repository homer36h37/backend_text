from database import Base
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, DateTime


# создаем модель, объекты которой будут храниться в бд
class Base(DeclarativeBase): pass

class Word(Base):
    __tablename__ = "words"

    word_id = Column(Integer, primary_key=True, index=True)
    word_count = Column(Integer,) # Количество слов
    description_name = Column(Text) # Слова в тексте
    create_date = Column(DateTime, nullable=False)

class WordStatistic(Base):
    __tablename__ = "words_statistic"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String) # Текст
    number = Column(Integer,) # Номер
    create_date = Column(DateTime, nullable=False)