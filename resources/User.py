from flask_restful import Resource
from flask import request, jsonify
from Model import db, User, UserSchema

users_schema = UserSchema(many=True)
user_schema = UserSchema()

class UserResource(Resource):
    def get(self):
        users = User.query.all()
        users = users_schema.dump(users)
        return {"status" : "success", "data" : users}, 200

    def post(self):
        json_data = request.get_json(force=True)

        if not json_data or not 'first_name' in json_data or not 'last_name' in json_data or not 'employee_id' in json_data:
            return {"error" : "Input data missing"}, 400
        
        user = User.query.filter_by(first_name=json_data['first_name'], last_name=json_data['last_name']).first()

        if user:
            return {'message': 'User already exists'}, 400
        
        user = User(
            first_name = json_data['first_name'],
            last_name = json_data['last_name'],
            employee_id = json_data['employee_id']
        )

        db.session.add(user)
        db.session.commit()

        result = user_schema.dump(user)

        return {"message" : "Saved successfully!", "data" : result}, 201

    def put(self):
        json_data = request.get_json(force=True)

        if not json_data or not 'id' in json_data:
            return {"error" : "Input data not provided"}, 400
        
        user = User.query.filter_by(id=json_data['id']).first()

        if not user:
            return {'message': 'User doe not exists'}, 400
        
        if 'first_name' in json_data:
            user.first_name = json_data['first_name']

        if 'last_name' in json_data:
            user.last_name = json_data['last_name']
        
        db.session.commit()

        result = user_schema.dump(user)

        return jsonify({"message" : "Updated Successfully!", "data" : result})

    def delete(self):
        json_data = request.get_json(force=True)

        if not json_data or not 'id' in json_data:
            return {"error" : "Id not provided"}, 400
        
        deleted_row = User.query.filter_by(id=json_data['id']).delete()

        db.session.commit()

        message = 'Deleted Successfully!' if deleted_row >0 else 'Failed to delete!'

        return jsonify({"message" : message})