from flask import Flask, render_template, request, jsonify, redirect
from deta import Deta

deta = Deta("DETA_SPACE_KEY")

db = deta.Base('recipes')

app = Flask(__name__,static_folder='static')

class Recipe:
    def __init__(self, name, ingredients, instructions,source):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions
        self.source = source
    
    def json(self):
        return {
            'name': self.name,
            'ingredients': self.ingredients,
            'instructions': self.instructions,
            'source': self.source
        }

@app.route('/')
def index():
    recipes = db.fetch()
    return render_template('index.html',recipes=recipes.items)

@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        recipe = Recipe(
            request.form['name'],
            request.form['ingredients'],
            request.form['instructions'],
            request.form['source']
        )
        db.put(recipe.json())
        recipe = db.fetch({'name': recipe.name}).items[0]
        return redirect(f'/recipe/{recipe["key"]}')
    return render_template('editor.html',recipe=None, link='/write')

@app.route('/delete/<id>')
def delete(id):
    db.delete(id)
    return redirect('/')

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    recipe = db.get(id)
    if request.method == 'POST':
        recipe['name'] = request.form['name']
        recipe['ingredients'] = request.form['ingredients']
        recipe['instructions'] = request.form['instructions']
        recipe['source'] = request.form['source']
        db.update(recipe,id)
        return redirect(f'/recipe/{id}')
    print(recipe)
    return render_template('editor.html', recipe=recipe, link=f'/edit/{id}')


@app.route('/search')
def search():
    search = request.args.get('q')
    if search:
        recipes = db.fetch({'name?contains': search})
        if recipes.count == 0:
            return {'message': 'No recipes found'}
        
        p = request.args.get('p')
        if p == 'html':
            return render_template('search.html', recipes=recipes.items, search=search)
        
        return jsonify(recipes.items)
    else:
        return {'message': 'No search query provided'}
    

@app.route('/recipe/<id>')
def recipe(id):
    get = db.get(id)
    return render_template('recipe.html', get=get)
