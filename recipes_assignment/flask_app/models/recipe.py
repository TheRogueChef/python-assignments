from flask_app.config.mysqlconnection import connect
from flask import flash
from flask_app.models import user
mydb = 'recipe_assignment'

class Recipe:
    def __init__ (self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.created_on = data ['created_on']
        self.updated_on = data['updated_on']
        self.userfk_id = data["userfk_id"]
        self.userfk = None

    
    @staticmethod
    def validate_recipe(recipe_data):
        is_valid = True
        # print(len(recipe_data['name']))
        if len(recipe_data['name']) < 1:
            is_valid = False
            flash('Please enter recipe name.')
        elif len(recipe_data['name']) < 4:
            is_valid = False
            flash("Recipe name must be ay least 2 characters.")
        if len(recipe_data['description']) < 1:
            is_valid = False
            flash('Description required.')
        elif len(recipe_data['description']) < 4:
            is_valid = False
            flash("Description must have at least 3 characters.")   
        if  len(recipe_data['instructions']) < 1:
            is_valid = False
            flash("Instructions required.")   
        elif len(recipe_data['instructions']) < 4:
            is_valid = False
            flash("Instructions must have at least 3 characters.")   
        return is_valid
    
    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO recipes
        (name, description, instructions, userfk_id)
        VALUES (%(name)s,%(description)s,%(instructions)s,%(userfk_id)s);
        """
        results = connect(mydb).query_db(query, data)
        print(results)
        
    @classmethod
    def get_all(cls):
        query = """
        SELECT *
        FROM recipes;"""
        results = connect(mydb). query_db(query)
        # print (results)
        if results == False:
            return []
        output = []
        for recipe_dictionary in results:
            print(recipe_dictionary)
            output.append(cls(recipe_dictionary))
        return output

    @classmethod
    def get_all_join_creator(cls):
        query = """
        SELECT *
        FROM recipes
        JOIN users
        ON recipes.userfk_id = users.id;
        """
        results = connect(mydb). query_db(query)
        if results == False:
            return []
        output = []
        for recipe_dictionary in results:
            print(recipe_dictionary)
            this_recipe = cls(recipe_dictionary)
            print(this_recipe)
            user_data = {
                    'id': recipe_dictionary['users.id'],
                    'first_name' : recipe_dictionary['first_name'],
                    'last_name' : recipe_dictionary['last_name'],
                    'email' : recipe_dictionary['email'],
                    'password' : recipe_dictionary['password'],
                    'created_on' : recipe_dictionary ['users.created_on'],
                    'updated_on' : recipe_dictionary['users.updated_on'] 
            }
            recipe_user = user.User(user_data)
            # print(recipe_user)
            this_recipe.userfk = recipe_user
            print(f"recipe.userfk_id: {this_recipe.userfk}")
            output.append(this_recipe)
        # print(output)
        return output
    
    @classmethod 
    def delete(cls, data):
        query = """
        DELETE FROM recipes
        WHERE id = %(id)s;
        """
        results = connect(mydb).query_db(query, data)
        
    @classmethod
    def get_by_id(cls, data):
        query = """
        SELECT * 
        FROM recipes
        WHERE id = %(id)s;
        """
        results = connect(mydb).query_db(query, data)
        return cls(results[0])
    
    @classmethod 
    def update(cls, data):
        query = """
        UPDATE recipes
        SET name = %(name)s,
        description = %(description)s,
        instructions = %(instructions)s
        WHERE id = %(id)s;
        """
        results = connect(mydb).query_db(query, data)