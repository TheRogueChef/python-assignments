from flask_app.config.mysqlconnection import connect
from flask import flash
from flask_app.models import user
mydb = 'Python_Exam_2'

class Band:
    def __init__ (self, data):
        self.id = data['id']
        self.name = data['name']
        self.genre = data['genre']
        self.city = data['city']
        self.created_on = data ['created_on']
        self.updated_on = data['updated_on']
        self.userfk_id = data["userfk_id"]
        self.userfk = None

    
    @staticmethod
    def validate_band(band_data):
        is_valid = True
        if len(band_data['name']) < 1:
            is_valid = False
            flash('Please enter band name.')
        elif len(band_data['name']) < 4:
            is_valid = False
            flash("Band name must be ay least 2 characters.")
        if len(band_data['genre']) < 1:
            is_valid = False
            flash('Genre required.')
        elif len(band_data['genre']) < 4:
            is_valid = False
            flash("Genre must have at least 3 characters.")   
        if  len(band_data['city']) < 1:
            is_valid = False
            flash("City required.")   
        elif len(band_data['city']) < 4:
            is_valid = False
            flash("City name must have at least 3 characters.")   
        return is_valid
    
    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO bands
        (name, genre, city, userfk_id)
        VALUES (%(name)s,%(genre)s,%(city)s,%(userfk_id)s);
        """
        results = connect(mydb).query_db(query, data)
        print(results)
        
    @classmethod
    def get_all(cls):
        query = """
        SELECT *
        FROM bands;"""
        results = connect(mydb). query_db(query)
        # print (results)
        if results == False:
            return []
        output = []
        for band_dictionary in results:
            print(band_dictionary)
            output.append(cls(band_dictionary))
        return output

    @classmethod
    def get_all_join_creator(cls):
        query = """
        SELECT *
        FROM bands
        JOIN users
        ON bands.userfk_id = users.id;
        """
        results = connect(mydb). query_db(query)
        print('get all', results)
        if results == False:
            return []
        output = []
        for band_dictionary in results:
            print(band_dictionary)
            this_band = cls(band_dictionary)
            print(this_band)
            user_data = {
                    'id': band_dictionary['users.id'],
                    'first_name' : band_dictionary['first_name'],
                    'last_name' : band_dictionary['last_name'],
                    'email' : band_dictionary['email'],
                    'password' : band_dictionary['password'],
                    'created_on' : band_dictionary ['users.created_on'],
                    'updated_on' : band_dictionary['users.updated_on'] 
            }
            band_user = user.User(user_data)
            print(band_user)
            this_band.userfk = band_user
            print(f"band.userfk: {this_band.userfk}")
            output.append(this_band)
        print(output)
        return output
    
    @classmethod 
    def delete(cls, data):
        query = """
        DELETE FROM bands
        WHERE id = %(id)s;
        """
        results = connect(mydb).query_db(query, data)
        
    @classmethod
    def get_by_id(cls, data):
        query = """
        SELECT * 
        FROM bands
        WHERE id = %(id)s;
        """
        results = connect(mydb).query_db(query, data)
        return cls(results[0])
    
    @classmethod 
    def update(cls, data):
        query = """
        UPDATE bands
        SET name = %(name)s,
        genre = %(genre)s,
        city = %(city)s
        WHERE id = %(id)s;
        """
        results = connect(mydb).query_db(query, data)