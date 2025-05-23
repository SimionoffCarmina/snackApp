from flask import Flask, jsonify, request
from dotenv import load_dotenv
import re

from models import category

load_dotenv()

from config import Config
from models import db
from models.category import Category
from models.recipe import Recipe
from models.ingredient import Ingredient
from models.association import recipe_category
from import_script import populate_db, get_all_recipes

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


@app.route('/')
def hello_world():
    return 'Welcome to SnackApp!'


@app.route('/api/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)

    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404

    return jsonify(recipe.recipe_json()), 200


def get_recipe_as_list():
    recipes = []
    for recipe in db.session.query(Recipe).all():
        recipes.append(recipe.recipe_json())
    return recipes


@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    recipes = get_recipe_as_list()
    return jsonify(recipes)


@app.route('/api/recipes', methods=['POST'])
def create_recipe():
    data = request.get_json()
    if data is None:
        return jsonify({'message': 'No input data provided'}), 400

    name = data.get('name')
    if not name or not isinstance(name, str) or name.strip() == "":
        return jsonify({'message': 'Name is required'}), 400

    duration = data.get('duration')
    if not duration or not isinstance(duration, str) or duration.strip() == "":
        return jsonify({'error': 'Duration must be a non-empty string'}), 400

    pictures = data.get('pictures')
    if not pictures or not isinstance(pictures, list) or not all(isinstance(pic, str) for pic in pictures):
        return jsonify({'message': 'Pictures are required as a list of valid URLs'}), 400

    instructions = data.get('instructions')
    if not instructions or not isinstance(instructions, str) or instructions.strip() == "":
        return jsonify({'message': 'Instructions are required'}), 400

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
        if cat:
            categories.append(cat)
        else:
            return jsonify({'message': f'Category {name} doesnt exist'}), 404

    ingredients = []
    ingredients_data = data.get('ingredients', [])
    for ingredient_str in ingredients_data:
        ingredient = Ingredient(
            name=ingredient_str['name'],
            unit=ingredient_str['unit'],
            quantity=ingredient_str['quantity']
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
    return jsonify({'message': 'Created a new recipe'}), 201


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
        if cat:
            categories.append(cat)
        else:
            return jsonify({'error': f'Category {name} doesnt exist'}), 400

    for ing in recipe.ingredients:
        db.session.delete(ing)
    db.session.flush()

    ingredients = []
    for ingredient in data.get('ingredients', []):
        ingredient = Ingredient(
            name=ingredient['name'],
            unit=ingredient['unit'],
            quantity=float(ingredient['quantity']),
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
    }, 201


@app.route('/api/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)

    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404

    for ingredient in recipe.ingredients:
        db.session.delete(ingredient)

    db.session.delete(recipe)
    db.session.commit()

    return jsonify({'message': 'Recipe deleted'}), 204


@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    category_data = []
    for c in categories:
        category_data.append(c.category_json())
    return jsonify({'categories': category_data}), 200


def is_valid_hex_color(hex_color):
    hex_color_regex = r'^#[0-9A-Fa-f]{6}$'
    return re.match(hex_color_regex, hex_color) is not None


@app.route('/api/categories', methods=['POST'])
def add_cat():
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'No input data provided'}), 400

    name = data.get('name')
    if name is None or not isinstance(name, str) or name.strip() == "":
        return jsonify({'error': 'No name provided'}), 400

    color = data.get('color', '#808080')
    if color and not is_valid_hex_color(color):
        return jsonify({'error': 'Invalid color format'}), 400

    existing = Category.query.filter_by(name=name).first()
    if existing:
        return jsonify({'error': f'Category already exists'}), 400

    cat = Category(name=name, color=color)
    db.session.add(cat)
    db.session.commit()

    return jsonify({'message': 'Created a new category'}), 201


if __name__ == '__main__':
    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()
    #
    # # Use the following line if you want to populate the database with sample data
    # populate_db(get_all_recipes(), app, db)

    app.run(host="0.0.0.0")
