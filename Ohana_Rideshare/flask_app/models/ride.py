from flask_app.config.mysqlconnection import connect
from flask_app.models import user
from flask import flash
mydb = 'ohana_rideshare'


class Ride:
    def __init__(self, data):
        self.id = data['id']
        self.destination = data['destination']
        self.pick_up = data['pick_up']
        self.ride_date = data['ride_date']
        self.details = data['details'] 
        self.created_at = data ['created_at']
        self.updated_at = data['updated_at'] 
        self.passenger_id = data ['passenger_id']
        self.rider_id = data['driver_id'] 
        self.passenger = None
        
    @classmethod
    def get_all_with_no_driver(cls):
        query = """
        SELECT *
        FROM rides
        JOIN users
        ON rides.passenger_id = users.id
        WHERE rides.driver_id IS NULL;
        """
        results = connect(mydb). query_db(query) 
        # print(results)
        output = []
        for row in results:
            # print(row)
            this_ride = cls(row)
            user_data = {
                'id' : row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row ['users.created_at'],
                'updated_at' : row['users.updated_at'] 
            }
            user_passenger = user.User(user_data)
            this_ride.passenger = user_passenger
            output.append(this_ride)
        return output
            

    
        
        
    @classmethod
    def save(cls, data):
        query = """
        Insert INTO rides (destination, pick_up, ride_date, details, passenger_id)
        VALUES (%(destination)s, %(pick_up)s, %(ride_date)s, %(details)s, %(passenger_id)s);
        """
        connect(mydb). query_db(query, data) 
        
    @staticmethod
    def validate_ride(request):
        is_valid = True
        if len(request['destination']) < 1:
            is_valid = False
            flash('Destination required') 
        elif len(request['destination']) <= 2:
            is_valid = False
            flash("Destination must be ay least 2 characters.")      
        if len(request['pick_up']) < 1:
            is_valid = False
            flash('Pick up location required')
        elif len(request['pick_up']) <= 2:
            is_valid = False
            flash("Pick up location must be ay least 2 characters.")   
        if len(request['ride_date']) < 1:
            is_valid = False
            flash('Ride date required')     
        if len(request['details']) < 1:
            is_valid = False
            flash('Details required')
        elif len(request['details']) <= 9:
            is_valid = False
            flash("Details must be ay least 9 characters.")   
        return is_valid
    
    @classmethod
    def delete(cls, data):
        query = """
        DELETE FROM rides
        WHERE id = %(id)s;
        """
        connect(mydb).query_db(query, data)
        
    @classmethod
    def add_driver(cls, data):
        query = """
        UPDATE rides
        SET driver_id = %(driver_id)s
        WHERE id = %(id)s
        """
        connect(mydb).query_db(query, data) 