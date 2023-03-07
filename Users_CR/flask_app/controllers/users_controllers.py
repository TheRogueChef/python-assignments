from flask_app import app
from flask import request, render_template, redirect
from flask_app.models.user import User

#SHOW ALL USERS
@app.route('/show')
def index():
    all_users = User.get_all()
    return render_template('index.html', all_users = all_users)

# # #SHOW SINGLE USER
@app.route('/user/show/<int:user_id>')
def user_single(user_id):
    user = User.show_user_by_id({'id': user_id})
    return render_template('user.html', user = user)
    
    
 #NEW USER   
@app.route('/userinfo', methods=['post'])
def save_user():
    print(request.form)
    User.save(request.form)
    return redirect('/show')
    
@app.route("/users/new")
def show_user():
    return render_template("form.html")


# #DELETE USER
@app.route("/user/delete/<int:user_id>")
def delete_user(user_id):
    # user = User.show_user_by_id({'id': user_id})
    User.delete_by_id({'id': user_id})
    return redirect('/show')



# @app.route('/deleteuser', methods=['post'])
# def remove_user(user_id):
#     output = []
#     User.delete_by_id({'id': user_id})
#     output.append
#     return redirect('/show')


#EDIT USER
@app.route("/users/<int:id>/edit")
def edit_user(id):
    data ={
        "id":id
        }
    return render_template("edit.html", user = User.show_user_by_id(data))


@app.route("/user/update", methods=['post'])
def update_user(): 
    print (request.form['id'])
    User.edit_by_id(request.form)
    return redirect("/show")




