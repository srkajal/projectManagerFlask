from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import constant

ma = Marshmallow()
db = SQLAlchemy()

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(250), nullable = False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable =False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
    category = db.relationship('Category', backref=db.backref('comments', lazy='dynamic'))

    def __init__(self, comment, category_id):
        self.comment = comment
        self.category_id = category_id

    def __prep__(self, comment, category):
        return "comment: " + comment.comment + "category:" +category.name  

class Category(db.Model):
    __tablename__='categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

class ParentTask(db.Model):
    __tablename__='parent_task'
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(50))

    class Meta:
        ordering = ('task_name', )

    def __str__(self):
        return self.task_name


class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    employee_id = db.Column(db.Integer)

    class Meta:
        ordering = ('first_name', )

    def __str__(self):
        return self.first_name


class Project(db.Model):
    __tablename__='project'
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(50))
    start_date = db.Column(db.Date())
    end_date = db.Column(db.Date())
    priority = db.Column(db.Integer)
    status = db.Column(db.String(15), default='ACTIVE')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('project', lazy='dynamic'))

    class Meta:
        ordering = ('project_name')

    def __str__(self):
        return self.project_name



class Task(db.Model):
    __tablename__='task'
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(50))
    start_date = db.Column(db.Date())
    end_date = db.Column(db.Date())
    priority = db.Column(db.Integer)
    status = db.Column(db.String(15), default='OPEN')
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete='CASCADE'), nullable=False, unique=False)
    project = db.relationship('Project', backref=db.backref('task', lazy='dynamic'))
    parent_id = db.Column(db.Integer, db.ForeignKey('parent_task.id', ondelete='CASCADE'), nullable=False, unique=False)
    parentTask = db.relationship('ParentTask', backref=db.backref('task', lazy='dynamic'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('task', lazy='dynamic'))

    class Meta:
        ordering = ('task_name', )

    def __str__(self):
        return self.task_name

class CategorySchema(ma.Schema):
    name = fields.String(required=True)
    id = fields.Integer()

class CommentSchema(ma.Schema):
    id = fields.Integer()
    comment = fields.String(required=True)
    creation_date = fields.DateTime()
    category_id = fields.Integer()
    category_name = fields.String()

class ParentTaskSchema(ma.Schema):
    task_name = fields.String(required=True)
    id = fields.Integer()

class UserSchema(ma.Schema):
    id = fields.Integer()
    first_name = fields.String(required=True)
    employee_id = fields.Integer()
    last_name = fields.String(required=True)

class ProjectSchema(ma.Schema):
    id = fields.Integer()
    project_name = fields.String(required=True)
    start_date = fields.Date()
    end_date = fields.Date()
    priority = fields.Integer()
    status = fields.String(required=True)
    user_id = fields.Integer()
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)

class TaskSchema(ma.Schema):
    id = fields.Integer()
    task_name = fields.String(required=True)
    start_date = fields.Date()
    end_date = fields.Date()
    priority = fields.Integer()
    status = fields.String(required=True)
    user_id = fields.Integer()
    project_id = fields.Integer()
    parent_id = fields.Integer()
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    project_name = fields.String(required=True)
    parent_task_name = fields.String(required=True)