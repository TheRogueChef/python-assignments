from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import user, recipe
dateFormat = "%#m/%#d/%Y %I:%M %p"
mydb = 'recipe_assignment'



@app.route('/recipe')
def dashboard():
    if 'user_id' in session:
        total_recipes = recipe.Recipe.get_all_join_creator()
        # total_users = user.User.get_by_id({'id': user_id})
        
        return render_template("dashboard.html", all_recipes = total_recipes, dtf = dateFormat)      
    return redirect("/")

@app.route('/recipe/new')
def new_recipe():
    if 'user_id' in session:
        # total_recipes = recipe.Recipe.get_all()
        return render_template('create.html')
    
@app.route('/recipe/create', methods=["post"])
def create_recipe():
    print(request.form)
    if recipe.Recipe.validate_recipe(request.form):
        recipe.Recipe.save('recipe_id')
        return redirect ('/recipe')
    return redirect ('/recipe/new')

@app.route('/recipe/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    if 'user_id' in session:
        recipe.Recipe.delete({'id': recipe_id})
    return redirect('/recipe')

@app.route('/recipe/edit/<int:recipe_id>')
def edit_recipe(recipe_id):
    return render_template('edit.html',
            recipe = recipe.Recipe.get_by_id({'id': recipe_id}))
    
@app.route('/recipe/update/<int:recipe_id>', methods=["post"])
def update_recipe(recipe_id):
    if 'user_id' in session:
        print(request.form)
    if recipe.Recipe.validate_recipe(request.form):
        data = {
            'name': request.form["name"],
            'description': request.form["description"],
            'instructions': request.form["instructions"],
            'id': recipe_id
        }
        recipe.Recipe.update(data)
        return redirect ('/recipe')   
    return redirect(f"/recipe/edit/{recipe_id}")


@app.route('/recipe/show/<int:recipe_id>')
def show_recipe(recipe_id):
        return render_template('show.html',
        recipe = recipe.Recipe.get_by_id({'id': recipe_id}))