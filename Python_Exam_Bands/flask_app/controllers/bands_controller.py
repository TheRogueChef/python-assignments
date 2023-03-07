from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import user, band
dateFormat = "%#m/%#d/%Y %I:%M %p"
mydb = 'Python_Exam_2'


@app.route('/band')
def dashboard():
    if 'user_id' in session:
        print (session["user_id"])
        total_bands = band.Band.get_all_join_creator()
        one_user = user.User.get_by_id({'id':session['user_id']})
        return render_template("dashboard.html", all_bands = total_bands, this_user = one_user, dtf = dateFormat)      
    return redirect("/")

@app.route('/band/new')
def new_band():
        print ('this is a new band',session["user_id"])
        one_user = user.User.get_by_id({'id':session['user_id']})
        return render_template('create.html')
    
@app.route('/band/create', methods=["post"])
def create_band():
        print ('this is something different',session["user_id"])
    # if 'user_id' in session:  
        if band.Band.validate_band(request.form):
            data = {
                'name': request.form["name"],
                'genre': request.form["genre"],
                'city': request.form["city"],
                'userfk_id': session['user_id']
            }
            print(data)
            band.Band.save(data)
            return redirect ('/band')
        return redirect ('/band')
    # return redirect ('/')

@app.route('/band/delete/<int:band_id>')
def delete_band(band_id):
    if 'user_id' in session:
        band.Band.delete({'id': band_id})
    return redirect('/band')

@app.route('/band/edit/<int:band_id>')
def edit_band(band_id):
    one_user = user.User.get_by_id({'id':session['user_id']})
    return render_template('edit.html',
            band = band.Band.get_by_id({'id': band_id}))
    
@app.route('/band/update/<int:band_id>', methods=["post"])
def update_band(band_id):
    if 'user_id' in session:
        print(request.form)
    if band.Band.validate_band(request.form):
        data = {
            'name': request.form["name"],
            'genre': request.form["genre"],
            'city': request.form["city"],
            'id': band_id
        }
        band.Band.update(data)
        return redirect ('/band')   
    return redirect(f"/band/edit/{band_id}")

@app.route('/band/show/<int:band_id>')
def show_band(band_id):
    total_bands = band.Band.get_all_join_creator()
    one_user = user.User.get_by_id({'id':session['user_id']})
    return render_template('show.html', all_bands =total_bands, this_user = one_user, band = band.Band.get_by_id({'id': band_id}))

# @app.route('/band/derby')
# def band_derby():
#     if 'user_id' in session:
#         total_bands = band.Band.get_all_join_creator()
#         return render_template("derby.html", all_bands = total_bands, dtf = dateFormat)      
#     return redirect("/")
