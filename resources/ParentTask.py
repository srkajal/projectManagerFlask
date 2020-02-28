from flask_restful import Resource
from flask import request, jsonify
from Model import db, ParentTask, ParentTaskSchema

parent_tasks_schema = ParentTaskSchema(many=True)
parent_task_schema = ParentTaskSchema()

class ParentTaskResource(Resource):
    def get(self):
        parentTasks = ParentTask.query.all()
        parentTasks = parent_tasks_schema.dump(parentTasks)
        return {"status" : "success", "data" : parentTasks}, 200

    def post(self):
        json_data = request.get_json(force=True)

        if not json_data or not 'task_name' in json_data:
            return {"error" : "No input data provided"}, 400
        
        parentTask = ParentTask.query.filter_by(task_name=json_data['task_name']).first()

        if parentTask:
            return {'message': 'ParentTask already exists'}, 400
        
        parentTask = ParentTask(
            task_name = json_data['task_name']
        )

        db.session.add(parentTask)
        db.session.commit()

        result = parent_task_schema.dump(parentTask)

        return {"message" : "Saved successfully!", "data" : result}, 201

    def put(self):
        json_data = request.get_json(force=True)

        if not json_data or not 'task_name' in json_data or not 'id' in json_data:
            return {"error" : "Id or task_name input data not provided"}, 400
        
        parentTask = ParentTask.query.filter_by(id=json_data['id']).first()

        if not parentTask:
            return {'message': 'ParentTask doe not exists'}, 400
        
        parentTask.task_name = json_data['task_name']
        db.session.commit()

        result = parent_task_schema.dump(parentTask)

        return jsonify({"message" : "Updated Successfully!", "data" : result})

    def delete(self):
        json_data = request.get_json(force=True)

        if not json_data or not 'id' in json_data:
            return {"error" : "Id not provided"}, 400
        
        deleted_row = ParentTask.query.filter_by(id=json_data['id']).delete()

        db.session.commit()

        message = 'Deleted Successfully!' if deleted_row >0 else 'Failed to delete!'

        return jsonify({"message" : message})