from flask import render_template, redirect, url_for
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Optional
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'placeanyvaluehere'
Bootstrap(app)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo-tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# db = sqlite3.connect("todo-tasks.db")
# cursor = db.cursor()
#cursor.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY, name varchar(250) NOT NULL, due_date varchar(250), owner varchar(250), descr varchar(1000), created_date varchar(250), category varchar(250), completed INTEGER)")


# Site design: 3 types of pages
# 1. Homepage - List existing tasks
    # Add New Task button at bottom right
# 2. Create/Edit Task form
    # Ability to dynamically add new category
# 3. Detailed view if you click on a task

# On a task, you can:
#  - Mark as complete (cross off OR delete)
#  - Edit Task form

# Task db table columns:
#  - Name
#  - Due date
#  - Owner
#  - Description
#  - Created date
#  - Category
#  - Completed?


# Category database table configuration
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(250), nullable=False)
    category_tasks = relationship("Tasks", back_populates="category")


# Tasks database table configuration
class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    due_date = db.Column(db.Date, nullable=True)
    owner = db.Column(db.String(250), nullable=True)
    descr = db.Column(db.String(1000), nullable=True)
    created_date = db.Column(db.Date, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    category = relationship("Category", back_populates="category_tasks")
    completed = db.Column(db.Boolean, default=False)


# New/Edit Task form
class NewTaskForm(FlaskForm):
    name = StringField('Task Name', validators=[DataRequired()])
    due_date = DateField('Due Date',
                         validators=[Optional()],
                         format='%Y-%m-%d')
    owner = StringField('Owner')
    descr = StringField('Description')
    category = SelectField('Category',
                           render_kw={'onchange': 'test(this.form.category)'})
    new_category_name = StringField('New Category Name')
    submit = SubmitField('Submit')


def get_category_choices():
    """ Helper function to dynamically generate choices for Category SelectField
    based on values in Category table of database """
    category_choices = [None]
    category_choices += [cat.category_name for cat in db.session.query(Category).all()]
    category_choices += ["Add New"]
    return category_choices


# Flask routes

@app.route("/")
def home():
    """ Homepage """
    all_tasks = db.session.query(Tasks).all()
    # render homepage listing all tasks
    return render_template("index.html", tasks=all_tasks)


@app.route('/add', methods=["GET", "POST"])
def add_task():
    """ Add new to-do task to the database """
    form = NewTaskForm()
    # dynamically generate choices for Category SelectField based on values in Category table of database
    form.category.choices = get_category_choices()
    category_choices = [None]
    category_choices += [cat.category_name for cat in db.session.query(Category).all()]
    category_choices += ["Add New"]
    form.category.choices = category_choices
    # form submitted
    if form.validate_on_submit():
        # new category to add to database
        if request.form.get("new_category_name"):
            new_category = Category(
                category_name=request.form.get("new_category_name")
            )
            db.session.add(new_category)
            new_task_category = new_category
        elif request.form.get("category"):
            new_task_category = db.session.query(Category).filter_by(category_name=request.form.get("category")).first()
        # add new task to database
        input_due_date = request.form.get("due_date")
        if input_due_date:
            input_due_date = datetime.strptime(input_due_date, '%Y-%m-%d')
        new_task = Tasks(
            name=request.form.get("name"),
            due_date=input_due_date if input_due_date else None,
            owner=request.form.get("owner"),
            descr=request.form.get("descr"),
            created_date=datetime.now(),
            category=new_task_category,
            completed=False
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('add.html', form=form)


@app.route('/task/<int:task_id>')
def display_task(task_id):
    """ Display detailed view for a task """
    task = db.session.query(Tasks).get(task_id)
    return render_template('task.html', task=task)


@app.route('/edit/<int:task_id>', methods=["GET", "POST"])
def edit_task(task_id):
    """ Edit to-do task details """
    task_to_edit = db.session.query(Tasks).get(task_id)
    edit_form = NewTaskForm(
        name=task_to_edit.name,
        due_date=task_to_edit.due_date,
        owner=task_to_edit.owner,
        descr=task_to_edit.descr,
        category=task_to_edit.category.category_name
    )
    edit_form.category.choices = get_category_choices()
    # edits submitted
    if edit_form.validate_on_submit():
        # new category to add to database
        if request.form.get("new_category_name"):
            new_category = Category(
                category_name=request.form.get("new_category_name")
            )
            db.session.add(new_category)
            new_task_category = new_category
        elif request.form.get("category"):
            new_task_category = db.session.query(Category).filter_by(category_name=request.form.get("category")).first()
        task_to_edit.name = edit_form.name.data
        if edit_form.due_date.data:
            task_to_edit.due_date = datetime.strptime(edit_form.due_date.data, '%Y-%m-%d')
        task_to_edit.owner = edit_form.owner.data
        task_to_edit.descr = edit_form.descr.data
        task_to_edit.category = new_task_category
        db.session.commit()
        return redirect(url_for('display_task', task_id=task_to_edit.id))
    # else display Edit form
    return render_template('add.html', form=edit_form, is_edit=True, task_name=task_to_edit.name)


@app.route('/task_complete/<int:task_id>')
def mark_task_complete(task_id):
    """ Mark a task as completed """
    task_to_update = db.session.query(Tasks).get(task_id)
    if task_to_update:
        # flip value of boolean
        task_to_update.completed = not task_to_update.completed
        db.session.commit()
    return redirect(url_for('home'))


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    """ Delete a task """
    task_to_delete = db.session.query(Tasks).get(task_id)
    # task found - delete it
    if task_to_delete:
        db.session.delete(task_to_delete)
        db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
