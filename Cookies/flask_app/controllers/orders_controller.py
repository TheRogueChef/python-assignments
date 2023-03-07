from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import order, user
dateFormat = "%#m/%#d/%Y %I:%M %p"
mydb = 'cookies_order'



@app.route('/cookies')
def dashboard():
    if 'user_id' in session:
        total_orders = order.Order.get_all_join_creator()
        return render_template("dashboard.html", all_orders = total_orders, dtf = dateFormat)
    return redirect("/")

@app.route('/order/new')
def new_order():
    total_orders = order.Order.get_all()
    return render_template('create.html', all_users=total_orders)
    
@app.route('/order/create', methods=["post"])
def create_order():
    print(request.form)
    if order.Order.validate_order(request.form):
        order.Order.save(request.form)
        return redirect ('/cookies')
    return redirect ('/order/new')

@app.route('/cookies/delete/<int:order_id>')
def delete_order(order_id):
    order.Order.delete({'id': order_id})
    return redirect('/cookies')

@app.route('/cookies/edit/<int:order_id>')
def edit_order(order_id):
    return render_template('edit.html',
            order = order.Order.get_by_id({'id': order_id}))
    
@app.route('/order/update/<int:order_id>', methods=["post"])
def update_order(order_id):
    print(request.form)
    if order.Order.validate_order(request.form):
        data = {
            'type': request.form["type"],
            'box_quantity': request.form["box_quantity"],
            'id': order_id
        }
        # update
        order.Order.update(data)
        return redirect ('/cookies')   
    return redirect(f"/cookies/edit/{order_id}")

@app.route('/user/show/<int:user_id>')
def show_user(user_id):
    return render_template('show.html', user = user.User.get_by_id({'id' : user_id}))
    