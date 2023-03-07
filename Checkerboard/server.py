from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def check_1():
    return render_template("checkerboard.HTML", row=8, col=8, color_one='red', color_two='black')

@app.route('/<int:x>')
def check_2(x):
    return render_template("checkerboard.HTML", row=x, col=8, color_one='red', color_two='black')

@app.route('/<int:x>/<int:y>')
def check_3(x,y):
    return render_template("checkerboard.HTML", row=x, col=y, color_one='red', color_two='black')

@app.route('/')
def hello_world():
    return 'Hello World!'





if __name__=="__main__":
    app.run(debug=True)

