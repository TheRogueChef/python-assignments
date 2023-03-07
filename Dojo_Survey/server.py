
from flask import Flask, render_template, redirect, session, request
app = Flask(__name__) 
app.secret_key = "secret"

User = [
        {'name' : 'Michael Choi'},
        {'location' : 'Seattle'},
        {'language' : 'Python!'},
        {'comment' : 'Hi There :)'}
    ]


@app.route('/')
def survey():
    return render_template('index.html')


    
@app.route('/process', methods=['POST'])
def process():
    print(request.form)
    session['name'] = request.form['name']
    session['location'] = request.form['location']
    session['language'] = request.form['language']
    session['comment'] = request.form['comment']
    return redirect("/result")



@app.route('/result')
def user_result():
    return render_template('result.html')

if __name__=="__main__":     
    app.run(debug=True) 