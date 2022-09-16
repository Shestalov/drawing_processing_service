from flask import Flask, request, flash, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from celery_worker import task1
import os
import os.path
import time
# import sqlite3
from flask_migrate import Migrate
from models import db, Test

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:example@127.0.0.1:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

migrate = Migrate(app, db, render_as_batch=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def uploads():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            task_obj = task1.delay(filename)

            # with sqlite3.connect('identifier.sqlite') as con:
            #     cur = con.cursor()
            #     cur.execute(f"""INSERT INTO task_state(task_id, file_name, status)
            #                                 VALUES ('{str(task_obj)}', '{filename}', 'added')""")
            #     con.commit()

            db.session.add(Test(task_id=str(task_obj), file_name=filename, status='added'))
            db.session.commit()

            time.sleep(3)  # wait when task resize the image
            return redirect(url_for('download_file', name=filename))

    return render_template("main_page.html")


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


if __name__ == '__main__':
    app.run()
