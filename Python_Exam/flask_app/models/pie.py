from flask_app.config.mysqlconnection import connect
from flask import flash
from flask_app.models import user
mydb = 'Python_Exam'

class Pie:
    def __init__ (self, data):
        self.id = data['id']
        self.name = data['name']
        self.filling = data['filling']
        self.crust = data['crust']
        self.created_on = data ['created_on']
        self.updated_on = data['updated_on']
        self.userfk_id = data["userfk_id"]
        self.userfk = None

    
    @staticmethod
    def validate_pie(pie_data):
        is_valid = True
        if len(pie_data['name']) < 1:
            is_valid = False
            flash('Please enter pie name.')
        elif len(pie_data['name']) < 4:
            is_valid = False
            flash("Pie name must be ay least 2 characters.")
        if len(pie_data['filling']) < 1:
            is_valid = False
            flash('Pie filling required.')
        elif len(pie_data['filling']) < 4:
            is_valid = False
            flash("Filling must have at least 3 characters.")   
        if  len(pie_data['crust']) < 1:
            is_valid = False
            flash("Crust required.")   
        elif len(pie_data['crust']) < 4:
            is_valid = False
            flash("Crust type must have at least 3 characters.")   
        return is_valid
    
    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO pies
        (name, filling, crust, userfk_id)
        VALUES (%(name)s,%(filling)s,%(crust)s,%(userfk_id)s);
        """
        results = connect(mydb).query_db(query, data)
        print(results)
        
    @classmethod
    def get_all(cls):
        query = """
        SELECT *
        FROM pies;"""
        results = connect(mydb). query_db(query)
        # print (results)
        if results == False:
            return []
        output = []
        for pie_dictionary in results:
            print(pie_dictionary)
            output.append(cls(pie_dictionary))
        return output

    @classmethod
    def get_all_join_creator(cls):
        query = """
        SELECT *
        FROM pies
        JOIN users
        ON pies.userfk_id = users.id;
        """
        results = connect(mydb). query_db(query)
        if results == False:
            return []
        output = []
        for pie_dictionary in results:
            print(pie_dictionary)
            this_pie = cls(pie_dictionary)
            print(this_pie)
            user_data = {
                    'id': pie_dictionary['users.id'],
                    'first_name' : pie_dictionary['first_name'],
                    'last_name' : pie_dictionary['last_name'],
                    'email' : pie_dictionary['email'],
                    'password' : pie_dictionary['password'],
                    'created_on' : pie_dictionary ['users.created_on'],
                    'updated_on' : pie_dictionary['users.updated_on'] 
            }
            pie_user = user.User(user_data)
            print(pie_user)
            this_pie.userfk = pie_user
            print(f"pie.userfk: {this_pie.userfk}")
            output.append(this_pie)
        print(output)
        return output
    
    @classmethod 
    def delete(cls, data):
        query = """
        DELETE FROM pies
        WHERE id = %(id)s;
        """
        results = connect(mydb).query_db(query, data)
        
    @classmethod
    def get_by_id(cls, data):
        query = """
        SELECT * 
        FROM pies
        WHERE id = %(id)s;
        """
        results = connect(mydb).query_db(query, data)
        return cls(results[0])
    
    @classmethod 
    def update(cls, data):
        query = """
        UPDATE pies
        SET name = %(name)s,
        filling = %(filling)s,
        crust = %(crust)s
        WHERE id = %(id)s;
        """
        results = connect(mydb).query_db(query, data)