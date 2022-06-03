import time
import redis
from flask import Flask
import pymysql
import psycopg2
import random


app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)
            
@app.route('/')
def start_page():
    return '<a href="/docker_primer">This is docker from guide</a><br><a href="/mysql">Thi is for MYSQL</a><br><a href="/postgres">Thi is for Postgres</a>'           

@app.route('/docker_primer')
def hello():
    count = get_hit_count()
    return 'Hello from Docker! I have been seen {} times.\n'.format(count)
    
@app.route('/mysql')
def mysql():
    connection = pymysql.connect(host='db', user='user', password='test', database='myDb', cursorclass=pymysql.cursors.DictCursor)
    name=[]
    res=''             
    try:              
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Laba")
            data = cursor.fetchall()
            for i in data:
                name.append(i.get('name'))
                tr = '<tr>'
                tr += '<td style="padding: 10px;">' + str(i.get('id')) + '</td>'
                tr += '<td style="padding: 10px;">' + str(i.get('name')) + '</td>'
                tr += '</tr>'
                res += tr
            rand=random.choice(name)
               
            return f"<h2>This page belongs to MYSQL<h2><h3>Все варианты лаборных работ:</h3><table style='border: 1px solid;'><tr><td style='padding: 10px;'>Номер</td><td style='padding: 10px;'>Название лабораторной работы</td></tr>{res}</table><br><br>Today you must do:{rand}<br><br>Обновите страницу, чтобы изменить решение"
    finally:
        connection.close()
@app.route('/postgres')
def postgres():
    connection = psycopg2.connect(host="postgres", database="postdb", user="user", password="test")
    connection.autocommit = True
    name=[]
    res=''             
    try:
        with connection.cursor() as cursor:
            try:
               
                cursor.execute( """CREATE TABLE Laba(
                                    id serial PRIMARY KEY,
                                    name varchar(32) NOT NULL,
                                    diff varchar(120) NOT NULL);""")
            except:
                pass
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO Laba(name, diff) VALUES('Laba1 Linux', 'easy');")
            cursor.execute("INSERT INTO Laba(name, diff) VALUES('Laba2 Linux', 'easy');")  
            cursor.execute("INSERT INTO Laba(name, diff) VALUES('Git', 'easy');")
            cursor.execute("INSERT INTO Laba(name, diff) VALUES('Docker', 'killed my linux twice: Lasciate ogne speranza, voi ch’entrate');")
        name=[]          
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Laba")
            data = cursor.fetchall()
            result = ''
            for i in data:
                name.append(str(i[1]))
                tr = '<tr>'
                tr += '<td style="padding: 10px;">' + str(i[0]) + '</td>'
                tr += '<td style="padding: 10px;">' + str(i[1]) + '</td>'
                tr += '<td style="padding: 10px;">' + str(i[2]) + '</td>'
                tr += '</tr>'
                res += tr
            rand=random.choice(name)
            return f"<h2>This page belongs to Postgres<h2><h3>Все варианты лаборных работ:</h3><table style='border: 1px solid;'><tr><td style='padding: 10px;'>Номер</td><td style='padding: 10px;'>Лабораторная работа</td><td style='padding: 10px;'>Сложность выполнения</td></tr>{res}</table><br><br>Today you must do:{rand}"
    finally:
        connection.close()
