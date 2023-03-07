from flask import Flask, render_template

app = Flask(__name__)

@app.route('/play')
def level_one():
    return render_template("index.html", num=3, color = "blue")

@app.route('/play/<int:num>')
def level_two(num):
    return render_template("index.html", num = num, color = "blue")

@app.route('/play/<int:num>/<string:color>')
def level_three(num, color):
    return render_template("index.html", num = num, color = color)

@app.route('/lists')
def render_lists():
    # Soon enough, we'll get data from a database, but for now, we're hard coding data
    student_info = [
        {'name' : 'Michael', 'age' : 35},
        {'name' : 'John', 'age' : 30 },
        {'name' : 'Mark', 'age' : 25},
        {'name' : 'KB', 'age' : 27}
    ]
    return render_template("lists.html", random_numbers = [3,1,5], students = student_info)




if __name__=="__main__":
    app.run(debug=True)