from flask import Flask, jsonify, request
from dotenv import load_dotenv
import re

load_dotenv()

from config import Config
from models import db
from models.category import Category
from models.recipe import Recipe
from models.ingredient import Ingredient
from models.association import recipe_category

CATEGORY_COLORS = {
    'Baking': '#FFA500',  # orange
    'Cookies': '#D2691E',  # chocolate
    'Pie': '#FFD700',  # gold
    'Italian': '#FF0000',  # red
    'No-bake': '#ADD8E6'  # lightblue
}

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def get_recipe_as_list():
    recipes = []
    for recipe in db.session.query(Recipe).all():
        recipes.append(recipe.as_dict())
    return recipes
@app.route('/')
def hello_world():
    return 'Welcome to SnackApp!'


@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    recipes = get_recipe_as_list()
    return jsonify(recipes)


@app.route('/api/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipes = get_recipe_as_list()
    for recipe in recipes:
        if recipe['id'] == recipe_id:
            return jsonify(recipe)
    return 'Recipe not found', 404


@app.route('/api/recipes', methods=['POST'])
def create_recipe():
    data = request.get_json()
    if data is None:
        return jsonify({'message': 'No input data provided'}), 400

    categories = []
    for name in data.get('categories', []):
        cat = Category.query.filter_by(name=name).first()
        if not cat:
            cat = Category(name=name)
            db.session.add(cat)
        categories.append(cat)

    ingredient_regex = re.compile(r'^(?P<quantity>\d+)(?P<unit>[a-zA-Z]*) (?P<name>.+)$')
    ingredients = []
    ingredients_data = data.get('ingredients', [])
    for ingredient_str in ingredients_data:
        match = ingredient_regex.match(ingredient_str.strip())
        if not match:
            return jsonify({'error': f'Invalid ingredient format: {ingredient_str}'}), 400

        ingredient = Ingredient(
            name=match['name'],
            unit=match['unit'] or None,
            quantity=float(match['quantity'])
        )
        ingredients.append(ingredient)


    new_recipe = Recipe(
        name = data.get('name'),
        duration = data.get('duration'),
        pictures = data.get('pictures'),
        instructions = data.get('instructions'),
        categories = categories,
        ingredients = ingredients
    )

    db.session.add(new_recipe)
    db.session.flush()

    for ing in ingredients:
        ing.recipe_id = new_recipe.id
        db.session.add(ing)

    db.session.commit()
    return "added recipe"


@app.route('/api/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)

    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404

    for ingredient in recipe.ingredients:
        db.session.delete(ingredient)

    db.session.delete(recipe)
    db.session.commit()

    return jsonify({'message': 'Recipe deleted'}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
