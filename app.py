from flask import Flask, render_template, request,redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) #create afalsk object 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite' #specify the db address in flask 
app.config['SQLALCHEMY_TRACK_MODIFCATIONS'] = False # speicfy other params SQLALCHEMY_TRACK_MODIFCATIONS
db = SQLAlchemy(app) # Create an object of SQLaclehmy with app as param

app.app_context().push()

class Todo(db.Model): #Create  the model of DB
    id = db.Column(db.Integer, primary_key =True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


# Its the display method from  Todoclass or DB
@app.route('/')
def index():
    todo_list = Todo.query.all() # Query the tODO CLASS
    print(todo_list) # print the values
    return render_template("index.html", todo_list=todo_list) # pass the value to the index.html 

# Its the method for creating new todo. Even though the route is hidden, we need to show it
@app.route('/add', methods=["POST"])
def add():
    title = request.form.get("title")  # Get the title from request
    new_todo =  Todo(title=title, complete=False) # create an object for title
    db.session.add(new_todo) # add the object to DB
    db.session.commit() # commit the db
    return redirect(url_for("index"))

@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()# commit the db
    return redirect(url_for("index"))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()# commit the db
    return redirect(url_for("index"))



if __name__ == "__main__":
    db.create_all() #create  the database
    new_todo = Todo(title = "todo 1", complete = False) #create object todo for class Todo
    db.session.add(new_todo) # add the object to db 
    db.session.commit() # commit the db
    app.run(debug =True) # run the flask function obj