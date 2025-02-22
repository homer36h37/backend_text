from typing import Annotated
from collections import Counter
from sqlalchemy.orm import Session
from starlette import status
from datetime import date
from models import Word, WordStatistic
from database import db


from fastapi import FastAPI, Depends, UploadFile

# приложение, которое ничего не делает
app = FastAPI(title="WordsStatisticApp",
    description="Information about words")

today = date.today()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]



@app.post("/uploadfile")
async def upload_file(uploaded_file: UploadFile):
    counter_words = 0
    str = ''
    words = []

    file = uploaded_file.file
    filename = uploaded_file.filename

    with open(filename, 'wb') as f:
        f.write(file.read())

    def func_words(words):
        myfile = open(filename)
        temp = []
        for line in myfile:
            temp += line.split()
            temp_var = temp[0]
        # эта движуха только для Windows с его суперкодировкой
        words.append(temp_var[3:])
        for i in temp[1:]:
            words.append(i)
        return words

    def func_counter(counter_words):
        file = func_words(words)
        for line in file:
            counter_words += len(line.split())
        return counter_words

    def func_stat():
        word_list = []
        for item in words:
            clear_word = ""
            for letter in item:
                if letter.isalpha():
                    clear_word += letter.lower()
            word_list.append(clear_word)
        return dict(Counter(word_list))


    def main():
        # print(type(func_counter(counter_words))) # <class 'int'>
        # print(type(words)) # <class 'list'>
        # print(type(func_stat())) # <class 'collections.Counter'>                                    

        temp_str = ''
        for i in words:
            temp_str += i + ' '
  

        p_word = Word(word_count=func_counter(counter_words), description_name=f"{temp_str}", create_date=today)
        db.add(p_word)     
        db.commit()   

        list = func_stat()

        for j in list.keys():
            s_word = WordStatistic(text=f"{j}", number=int(f"{list[f'{j}']}"), create_date=today)
            db.add(s_word)     
            db.commit()    



        return {
            "code":200,
            "status":"success",
            "data":[  
                {  
                    "formdata":"application/json"
                }
            ]
        }


    return main()
 
    
@app.get('/statistics', status_code=status.HTTP_200_OK)
async def read_all_inf(db: db_dependency):
    return db.query(Word).all()

@app.get('/wstatistics', status_code=status.HTTP_200_OK)
async def read_all_inf(db: db_dependency):
    return db.query(WordStatistic).all()