from flask_app.config.mysqlconnection import connect
from flask import flash
from flask_app.models import user
mydb = 'cookies_order'

class Order:
    def __init__ (self, data):
        self.id = data['id']
        self.type = data['type']
        self.box_quantity = data['box_quantity']
        self.created_at = data ['created_at']
        self.updated_at = data['updated_at']
        self.creator_id = data['creator_id']
        self.creator = None
    
    @staticmethod
    def validate_order(order_data):
        is_valid = True
        print(len(order_data['type']))
        if len(order_data['type']) < 1:
            is_valid = False
            flash('Please enter a cookie type.')
        elif len(order_data['type']) < 2:
            is_valid = False
            flash("Cookie type must be ay least 2 characters.")
        if len(order_data['box_quantity']) < 1:
            is_valid = False
            flash('Quantity required.')
        elif int(order_data['box_quantity']) <= 0:
            is_valid = False
            flash("Quantity must be at least one box.")   
        return is_valid
    
    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO orders
        (type, box_quantity, creator_id)
        VALUES (%(type)s,%(box_quantity)s,%(creator_id)s);
        """
        results = connect(mydb).query_db(query, data)
        print(results)
        
    @classmethod
    def get_all(cls):
        query = """
        SELECT *
        FROM orders;"""
        results = connect(mydb). query_db(query)
        # print (results)
        if results == False:
            return []
        output = []
        for order_dictionary in results:
            print(order_dictionary)
            output.append(cls(order_dictionary))
        return output

    @classmethod
    def get_all_join_creator(cls):
        query = """
        SELECT *
        FROM orders
        JOIN users
        ON orders.creator_id = users.id;"""
        results = connect(mydb). query_db(query)
        # print (results)
        if results == False:
            return []
        output = []
        for order_dictionary in results:
            print(order_dictionary)
            this_order = cls(order_dictionary)
            print(this_order)
            user_data = {
                    'id': order_dictionary['users.id'],
                    'first_name' : order_dictionary['first_name'],
                    'last_name' : order_dictionary['last_name'],
                    'email' : order_dictionary['email'],
                    'password' : order_dictionary['password'],
                    'created_at' : order_dictionary ['users.created_at'],
                    'updated_at' : order_dictionary['users.updated_at'] 
            }
            order_user = user.User(user_data)
            print(order_user)
            this_order.creator = order_user
            print(f"order.creator: {this_order.creator}")
            output.append(this_order)
        print(output)
        return output
    
    @classmethod 
    def delete(cls, data):
        query = """
        DELETE FROM orders
        WHERE id = %(id)s;
        """
        results = connect(mydb).query_db(query, data)
        
    @classmethod
    def get_by_id(cls, data):
        query = """
        SELECT * 
        FROM orders
        WHERE id = %(id)s;
        """
        results = connect(mydb).query_db(query, data)
        return cls(results[0])
    
    @classmethod 
    def update(cls, data):
        query = """
        UPDATE orders
        SET type = %(type)s,
        box_quantity = %(box_quantity)s
        WHERE id = %(id)s;
        """
        results = connect(mydb).query_db(query, data)

        