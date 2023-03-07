from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import user, pie
dateFormat = "%#m/%#d/%Y %I:%M %p"
mydb = 'Python_Exam'


@app.route('/pie')
def dashboard():
    if 'user_id' in session:
        total_pies = pie.Pie.get_all_join_creator()
        one_user = user.User.get_by_id({'id':session["user_id"]})
        return render_template("dashboard.html", all_piess = total_pies, the_user = one_user, dtf = dateFormat)      
    return redirect("/")

@app.route('/pie/new')
def new_pie():
        return render_template('create.html')
    
@app.route('/pie/create', methods=["post"])
def create_pie():
    if 'user_id' in session:
        if pie.Pie.validate_pie(request.form):
            data = {
                'name': request.form["name"],
                'filling': request.form["filling"],
                'crust': request.form["crust"],
                'userfk_id': session['user_id']
            }
            pie.Pie.save(data)
            return redirect ('/pie')
        return redirect ('/pie')
    return redirect ('/')

@app.route('/pie/delete/<int:band_id>')
def delete_pie(pie_id):
    if 'user_id' in session:
        pie.Pie.delete({'id': pie_id})
    return redirect('/pie')

@app.route('/pie/edit/<int:band_id>')
def edit_pie(pie_id):
    return render_template('edit.html',
            band = pie.Pie.get_by_id({'id': pie_id}))
    
@app.route('/pie/update/<int:pie_id>', methods=["post"])
def update_pie(pie_id):
    if 'user_id' in session:
        print(request.form)
    if pie.Pie.validate_pie(request.form):
        data = {
            'name': request.form["name"],
            'filling': request.form["filling"],
            'crust': request.form["crust"],
            'id': pie_id
        }
        pie.Pie.update(data)
        return redirect ('/pie')   
    return redirect(f"/pie/edit/{pie_id}")

@app.route('/pie/show/<int:pie_id>')
def show_pie(pie_id):
    one_user = user.User.get_by_id({'id':session["user_id"]})
    return render_template('show.html', the_user = one_user, pie = pie.Pie.get_by_id({'id': pie_id}))

@app.route('/pie/derby')
def pie_derby():
    if 'user_id' in session:
        total_pies = pie.Pie.get_all_join_creator()
        return render_template("derby.html", all_piess = total_pies, dtf = dateFormat)      
    return redirect("/")


