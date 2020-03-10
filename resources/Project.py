from flask_restful import Resource
from flask import request, jsonify
from Model import db, Project, ProjectSchema, User
from datetime import datetime
from HelperUtil import HelperUtil
import constant

projects_schema = ProjectSchema(many=True)
project_schema = ProjectSchema()

class ProjectResource(Resource):
    def get(self):
        projects = Project.query.all()
        
        projectsView = []

        for project in projects:
            projectView = {
                "id" : project.id,
                "project_name" : project.project_name,
                "start_date" : project.start_date,
                "end_date" : project.end_date,
                "priority" : project.priority,
                "status" : project.status,
                "user_id" : project.user_id,
                "first_name" : project.user.first_name,
                "last_name" : project.user.last_name
            }

            projectsView.append(projectView)

        projects = projects_schema.dump(projectsView)
        return {"status" : "success", "data" : projects}, 200

    def post(self):
        json_data = request.get_json(force=True)

        if not json_data or not 'project_name' in json_data or not 'start_date' in json_data or not 'end_date' in json_data or not 'priority' in json_data or not 'user_id' in json_data:
            return {"error" : "Input data missing"}, 400
        
        project = Project.query.filter_by(project_name=json_data['project_name']).first()

        if project:
            return {'message': 'Project already exists'}, 400

        user = User.query.filter_by(id=json_data['user_id']).first()

        if not user:
            return {'message': 'User doest not exist'}, 400
 
        project = Project(
            project_name = json_data['project_name'],
            start_date = HelperUtil.stringToDate(self, json_data['start_date']),
            end_date = HelperUtil.stringToDate(self, json_data['end_date']),
            priority = json_data['priority'],
            status = constant.ACTIVE,
            user_id = json_data['user_id']
        )

        db.session.add(project)
        db.session.commit()

        result = project_schema.dump(project)

        return {"message" : "Saved successfully!", "data" : result}, 201

    def put(self):
        json_data = request.get_json(force=True)

        if not json_data or not 'id' in json_data:
            return {"error" : "Input data not provided"}, 400
        
        project = Project.query.filter_by(id=json_data['id']).first()

        if not project:
            return {'message': 'Project doe not exists'}, 400
        
        if 'start_date' in json_data:
            project.start_date = HelperUtil.stringToDate(self, json_data['start_date'])

        if 'end_date' in json_data:
            project.end_date = HelperUtil.stringToDate(self, json_data['end_date'])

        if 'priority' in json_data:
            project.priority = json_data['priority']

        if 'status' in json_data:
            if not json_data['status'] in [constant.ACTIVE, constant.SUSPENDED]:
                return {'message': 'Invalid status'}, 400
            project.status = json_data['status']
        
        db.session.commit()

        result = project_schema.dump(project)

        return jsonify({"message" : "Updated Successfully!", "data" : result})

    def delete(self):
        json_data = request.get_json(force=True)

        if not json_data or not 'id' in json_data:
            return {"error" : "Id not provided"}, 400
        
        deleted_row = Project.query.filter_by(id=json_data['id']).delete()

        db.session.commit()

        message = 'Deleted Successfully!' if deleted_row >0 else 'Failed to delete!'

        return jsonify({"message" : message})