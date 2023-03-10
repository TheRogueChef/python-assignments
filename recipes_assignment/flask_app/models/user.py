from flask_app.config.mysqlconnection import connect
from flask_app.models import recipe
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
mydb = 'recipe_assignment'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password'] 
        self.created_on = data ['created_on']
        self.updated_on = data['updated_on'] 


        
    @classmethod
    def get_all(cls):
        query = """
        SELECT *
        FROM users;"""
        results = connect(mydb). query_db(query)
        output = []
        for user_dictionary in results:
            output.append(cls(user_dictionary))
        return output
    
    @classmethod
    def save(cls, data):
        query = """
        Insert INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        user_id = connect(mydb). query_db(query, data)

    # @classmethod
    # def get_by_id(cls, data):
    #     query = """
    #     SELECT *
    #     FROM users
    #     WHERE users.id = %(id)s;
    #     """
    #     results = connect(mydb). query_db(query, data)
    #     this_user = cls(results[0])
    #     return this_user
    
    @classmethod
    def get_by_id(cls, data):
        query = """
        SELECT *
        FROM users
        JOIN recipes
        ON recipes.userfk_id = users.id;
        """
        results = connect(mydb). query_db(query, data)
        print (results)
        this_user = cls(results[0])
        print(this_user)
        for row in results:
            recipe_data = {
                    'id' : row['recipes.id'],
                    'name' : row['name'],
                    'description' : row['description'],
                    'instructions' : row['instructions'],
                    'created_on' : row['recipes.created_on'],
                    'updated_on' : row['recipes.updated_on'],
                    'userfk_id': row['userfk_id']
                        }
        this_recipe = recipe.Recipe(recipe_data)
        print(this_recipe)
        this_user.recipes.append(this_recipe)
        print(this_user.recipes)
        return this_user
    
    @staticmethod
    def validate_user(request):
        is_valid = True
        if len(request['first_name']) < 1:
            is_valid = False
            flash('First name required', "regError") 
        elif len(request['first_name']) < 2:
            is_valid = False
            flash("First name must be ay least 2 characters.", 'regError')      
        if len(request['last_name']) < 1:
            is_valid = False
            flash('Last name required', "regError")
        elif len(request['last_name']) < 2:
            is_valid = False
            flash("Last name must be ay least 2 characters.", 'regError')   
        if len(request['email']) < 1:
            is_valid = False
            flash('Email required', "regError") 
        elif not EMAIL_REGEX.match(request['email']): 
            is_valid = False
            flash('Invalid email', "regError")    
        if len(request['password']) < 1:
            is_valid = False
            flash('Password required', "regError")
        elif len(request['password']) <= 4:
            is_valid = False
            flash("Password must be ay least 8 characters.", 'regError')
        elif request['password'] != request['passConf']:
            is_valid = False
            flash('Passwords must match', "regError")
        if User.get_by_email(request):
            is_valid = False
            flash('Try another email.', "regError")
        return is_valid   
    
    @classmethod
    def get_by_email(cls,data):
        query = """
        SELECT * 
        FROM users 
        WHERE email = %(email)s;
        """
        results = connect(mydb).query_db(query,data)
        # print(results)
        if len(results) < 1:
            return False
        return cls(results[0])
