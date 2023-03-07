from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = "secret key"

@app.route('/')
def counter():
    if "count" not in session:
        session["count"] = 0
    else:
        session['count'] += 1    
    return render_template('index.html', )

@app.route('/destroy_session')
def destroy():
    session.clear()
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)


