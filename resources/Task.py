from flask_restful import Resource
from flask import request, jsonify
from Model import db, Task, TaskSchema, User, Project, ParentTask
from datetime import datetime
from HelperUtil import HelperUtil
import constant

tasks_schema = TaskSchema(many=True)
task_schema = TaskSchema()

class TaskResource(Resource):
    def get(self):
        tasks = Task.query.all()
        
        tasksView = []

        for task in tasks:
            taskView = {
                "id" : task.id,
                "task_name" : task.task_name,
                "start_date" : task.start_date,
                "end_date" : task.end_date,
                "priority" : task.priority,
                "status" : task.status,
                "user_id" : task.user_id,
                "project_id" : task.project_id,
                "parent_id" : task.parent_id,
                "first_name" : task.user.first_name,
                "last_name" : task.user.last_name,
                "project_name" : task.project.project_name,
                "parent_task_name" : task.parentTask.task_name
            }

            tasksView.append(taskView)

        tasks = tasks_schema.dump(tasksView)
        return {"status" : "success", "data" : tasks}, 200

    def post(self):
        json_data = request.get_json(force=True)

        if not json_data or not 'task_name' in json_data or not 'start_date' in json_data or not 'end_date' in json_data or not 'priority' in json_data or not 'user_id' in json_data or not 'project_id' in json_data or not 'parent_id' in json_data:
            return {"error" : "Input data missing"}, 400
        
        task = Task.query.filter_by(task_name=json_data['task_name']).first()

        if task:
            return {'message': 'Task already exists'}, 400

        user = User.query.filter_by(id=json_data['user_id']).first()

        if not user:
            return {'message': 'User doest not exist'}, 400

        project = Project.query.filter_by(id=json_data['project_id']).first()

        if not project:
            return {'message': 'Project doest not exist'}, 400

        parentTask = ParentTask.query.filter_by(id=json_data['parent_id']).first()

        if not parentTask:
            return {'message': 'Parent task doest not exist'}, 400
 
        task = Task(
            task_name = json_data['task_name'],
            start_date = HelperUtil.stringToDate(self, json_data['start_date']),
            end_date = HelperUtil.stringToDate(self, json_data['end_date']),
            priority = json_data['priority'],
            status = constant.ACTIVE,
            user_id = json_data['user_id'],
            parent_id = json_data['parent_id'],
            project_id = json_data['project_id']
            
        )

        db.session.add(task)
        db.session.commit()

        result = task_schema.dump(task)

        return {"message" : "Saved successfully!", "data" : result}, 201

    def put(self):
        json_data = request.get_json(force=True)

        if not json_data or not 'id' in json_data:
            return {"error" : "Input data not provided"}, 400
        
        task = Task.query.filter_by(id=json_data['id']).first()

        if not task:
            return {'message': 'Task doe not exists'}, 400
        
        if 'start_date' in json_data:
            task.start_date = HelperUtil.stringToDate(self, json_data['start_date'])

        if 'end_date' in json_data:
            task.end_date = HelperUtil.stringToDate(self, json_data['end_date'])

        if 'priority' in json_data:
            task.priority = json_data['priority']

        if 'status' in json_data:
            if not json_data['status'] in [constant.OPEN, constant.CLOSED]:
                return {'message': 'Invalid status'}, 400
            task.status = json_data['status']
        
        db.session.commit()

        result = task_schema.dump(task)

        return jsonify({"message" : "Updated Successfully!", "data" : result})

    def delete(self):
        json_data = request.get_json(force=True)

        if not json_data or not 'id' in json_data:
            return {"error" : "Id not provided"}, 400
        
        deleted_row = Task.query.filter_by(id=json_data['id']).delete()

        db.session.commit()

        message = 'Deleted Successfully!' if deleted_row >0 else 'Failed to delete!'

        return jsonify({"message" : message})