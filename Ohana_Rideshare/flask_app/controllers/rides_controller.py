from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import ride
dateFormat = "%#m/%#d/%Y %I:%M %p"

@app.route('/ride/new')
def add_ride():
    return render_template('create.html')

@app.route ('/ride/create', methods=['post'])
def create_ride():
    if'user_id' in session:
        if ride.Ride.validate_ride(request.form):
            pass
            # save ride info
            data = {
                'destination' : request.form['destination'],
                'pick_up' : request.form['pick_up'],
                'ride_date' : request.form['ride_date'],
                'details' : request.form['details'],
                'passenger_id' : session['user_id']
            }
            print(data)
            ride.Ride.save(data)
            return redirect("/landing")
        return redirect("/ride/new")
    return redirect("/")
    
    
@app.route('/ride/delete/<int:ride_id>')
def delete_ride(ride_id):
    if 'user_id' in session:
        ride.Ride.delete({'id':ride_id})
        return redirect('/landing')
    return redirect('/')

@app.route('/ride/drive/<int:ride_id>')
def add_driver(ride_id):
    data = {
        'id' : ride_id,
        'driver_id' : session('/user_id')
    }
    ride.Ride.add_driver()
    return redirect("/landing")