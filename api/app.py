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
    categories_data = data.get('categories', [])
    for category in categories_data:
        if isinstance(category, str):
            name = category
            color = '#808080'
        elif isinstance(category, dict):
            name = category['name']
            color = category.get('color', '#808080')
        else:
            return jsonify({'message': 'Invalid format'}), 400
        if not name:
            jsonify({'message': 'No name provided'}), 400
        cat = Category.query.filter_by(name=name).first()
        if not cat:
            cat = Category(name=name, color=color)
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
        name=data.get('name'),
        duration=data.get('duration'),
        pictures=','.join(data['pictures']),
        instructions=data.get('instructions'),
        categories=categories,
        ingredients=ingredients
    )

    db.session.add(new_recipe)
    db.session.flush()

    for ing in ingredients:
        ing.recipe_id = new_recipe.id
        db.session.add(ing)

    db.session.commit()
    return jsonify({'message': 'Created a new recipe'}), 200


@app.route('/api/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)

    if not recipe:
        return jsonify({'message': 'Recipe not found'}), 404

    data = request.get_json()

    if data is None:
        return jsonify({'message': 'No input data provided'}), 400

    categories = []
    for category in data.get('categories', []):
        name = category.get('name')
        color = category.get('color', '#808080')
        cat = Category.query.filter_by(name=name).first()
        if not cat:
            cat = Category(name=name, color=color)
            db.session.add(cat)
        categories.append(cat)

    for ing in recipe.ingredients:
        db.session.delete(ing)
    db.session.flush()

    ingredients = []
    ingredient_regex = re.compile(r'^(?P<quantity>\d+)(?P<unit>[a-zA-Z]*) (?P<name>.+)$')
    for ingredient in data.get('ingredients', []):
        match = ingredient_regex.match(ingredient.strip())
        if not match:
            return jsonify({'error': f'Invalid ingredient format: {ingredient}'}), 400
        ingredient = Ingredient(
            name=match['name'],
            unit=match['unit'] or None,
            quantity=float(match['quantity']),
            recipe=recipe
        )
        ingredients.append(ingredient)

    recipe.name = data.get('name')
    recipe.duration = data.get('duration')
    recipe.pictures = data.get('pictures')
    recipe.instructions = data.get('instructions')
    recipe.categories = categories
    recipe.ingredients = ingredients

    db.session.commit()

    return {
        'id': recipe.id,
        'name': recipe.name,
        'duration': recipe.duration,
        'pictures': recipe.pictures,
        'instructions': recipe.instructions,
        'categories': [category.name for category in recipe.categories],
        'ingredients': [ingredient.name for ingredient in recipe.ingredients],
    }


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
