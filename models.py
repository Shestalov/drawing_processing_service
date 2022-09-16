from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Test(db.Model):
    __tablename__ = "test"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False, unique=True)
    task_id = db.Column(db.String(50), nullable=False)
    file_name = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return '<Test %r>' % self.id

    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'file_name': self.file_name,
            'status': self.status
        }
