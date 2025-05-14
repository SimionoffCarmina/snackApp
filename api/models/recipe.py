from models import db
from models.association import recipe_category
from models.category import Category


class Recipe(db.Model):
    def recipe_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'duration': self.duration,
            'pictures': self.pictures.split(',') if self.pictures else [],
            'categories': [
                {
                    'id': cat.id,
                    'name': cat.name,
                    'color': cat.color
                } for cat in self.categories
            ],
            'ingredients': [
                {
                    'id': ingr.id,
                    'name': ingr.name,
                    'unit': ingr.unit,
                    'quantity': ingr.quantity,
                } for ingr in self.ingredients
            ]
        }

    __tablename__ = 'recipe'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    pictures = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)

    categories = db.relationship('Category', secondary=recipe_category, backref=db.backref('recipes', lazy='dynamic'))

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}
