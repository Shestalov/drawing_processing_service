from celery import Celery
from PIL import Image

app = Celery('celery_worker', broker='pyamqp://guest@localhost//')


@app.task()
def task1(filename):
    img = Image.open('E:/hillel_python_pro/mycelery/uploads/' + filename)
    img = img.resize((512, 512), Image.ANTIALIAS)
    img.save('E:/hillel_python_pro/mycelery/uploads/' + filename)
