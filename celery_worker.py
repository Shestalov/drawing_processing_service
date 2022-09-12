from celery import Celery
from PIL import Image
import sqlite3
import time

app = Celery('celery_worker', broker='pyamqp://guest@localhost//')


@app.task()
def task1(filename):
    img = Image.open('uploads/' + filename)  # E:/hillel_python_pro/image_processing_service/
    img = img.resize((512, 512), Image.ANTIALIAS)
    img.save('uploads/' + filename)  # E:/hillel_python_pro/image_processing_service/

    time.sleep(1)  # wait when app write data in database

    with sqlite3.connect('identifier.sqlite') as con:
        cur = con.cursor()
        cur.execute(f"""UPDATE task_state SET status='resized', file_name= WHERE file_name='{filename}';""")
        con.commit()
