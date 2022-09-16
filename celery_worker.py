from celery import Celery
from PIL import Image
# import sqlite3
import time
import psycopg2

app2 = Celery('celery_worker', broker='pyamqp://guest@localhost//')


@app2.task()
def task1(filename):
    img = Image.open('uploads/' + filename)
    img = img.resize((512, 512), Image.ANTIALIAS)
    img.save('uploads/' + filename)

    time.sleep(2)  # wait when app write data in database

    # with sqlite3.connect('identifier.sqlite') as con:
    #     cur = con.cursor()
    #     cur.execute(f"""UPDATE task_state SET status='resized', file_name= WHERE file_name='{filename}';""")
    #     con.commit()

    update_status(filename)


def update_status(filename):
    conn = psycopg2.connect(
        host="127.0.0.1",
        database="postgres",
        user="postgres",
        password="example",
        port=5432)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    cur.execute(f"""UPDATE test SET status='resized' WHERE file_name='{filename}'""")

    conn.commit()
    cur.close()
    conn.close()
