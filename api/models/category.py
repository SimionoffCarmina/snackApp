from models import db


class Category(db.Model):
    def category_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color
        }

    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    color = db.Column(db.String(50), nullable=False)
