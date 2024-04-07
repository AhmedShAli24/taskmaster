import os
from flask import Flask,session,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite"

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    date = db.Column(db.Date)

with app.app_context():
    db.create_all()

@app.get('/')
def home():
    task_list = db.session.query(Task).all()
    return render_template('index.html', task_list = task_list)

@app.post("/add")
def add_task():
    new_task = request.form.get("task")
    task_date = datetime.now().date()
    task = Task(task = new_task, complete = False, date = task_date)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for("home"))

@app.get("/update/<int:task_id>")
def update(task_id):
    task = db.session.query(Task).filter(Task.id == task_id).first()
    task.complete = not task.complete
    db.session.commit()
    return redirect(url_for("home"))
    
@app.get("/delete/<int:task_id>")
def delete(task_id):
    task = db.session.query(Task).filter(Task.id == task_id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)