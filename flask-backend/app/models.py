from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TeaLeaf(db.Model):
    __tablename__ = 'tea_leaves'

    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(255), nullable=False)
    maturity_level = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<TeaLeaf {self.id} - {self.maturity_level}>'