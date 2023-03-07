from flask_app.config.mysqlconnection import connectToMySQL
mydb = 'users_schema'

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
      
#SHOW ALL USERS        
    @classmethod
    def get_all(cls):
        query = '''
        SELECT * 
        FROM users_schema.users;'''
        results = connectToMySQL(mydb).query_db(query)            
        print(results)
        output = []
        for user_dictionary in results:
            print(user_dictionary)
            output.append(cls(user_dictionary))
        return (output)
    
    
#NEW USER
    @classmethod
    def save(cls, data):
        query='''
        INSERT INTO users
        (first_name, last_name, email)
        VALUES (%(first_name)s,%(last_name)s,%(email)s);
        '''
        results = connectToMySQL(mydb).query_db(query, data)
        print(results)
        
#EDIT USER
    @classmethod
    def edit_by_id(cls, data):
        query='''
        UPDATE users
        SET first_name=%(first_name)s, last_name =%(last_name)s, email=%(email)s
        WHERE id = %(id)s;
        '''
        results = connectToMySQL(mydb).query_db(query, data)
        print(results)    
        
#DELETE USER
    @classmethod
    def delete_by_id(cls, data):
        query='''
        DELETE 
        FROM users
        WHERE id = %(id)s;
        '''
        results = connectToMySQL(mydb).query_db(query, data)

        
#SHOW SINGLE USER
    @classmethod
    def show_user_by_id(cls, data):
        query='''
        SELECT *
        FROM users
        WHERE id = %(id)s;
        '''
        results = connectToMySQL(mydb).query_db(query, data)
        print(results)
        return(cls(results[0]))
