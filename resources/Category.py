from flask_restful import Resource
from flask import request, jsonify
from Model import db, Category, CategorySchema

categories_schema = CategorySchema(many=True)
category_schema = CategorySchema()

class CategoryResource(Resource):
    def get(self):
        categories = Category.query.all()
        categories = categories_schema.dump(categories)
        return {"status" : "success", "data" : categories}, 200

    def post(self):
        json_data = request.get_json(force=True)

        if not json_data or not 'name' in json_data:
            return {"error" : "No input data provided"}, 400
        
        category = Category.query.filter_by(name=json_data['name']).first()

        if category:
            return {'message': 'Category already exists'}, 400
        
        category = Category(
            name = json_data['name']
        )

        db.session.add(category)
        db.session.commit()

        result = category_schema.dump(category)

        return {"message" : "Saved successfully!", "data" : result}, 201

    def put(self):
        json_data = request.get_json(force=True)

        if not json_data or not 'name' in json_data or not 'id' in json_data:
            return {"error" : "Id or Name input data not provided"}, 400
        
        category = Category.query.filter_by(id=json_data['id']).first()

        if not category:
            return {'message': 'Category doe not exists'}, 400
        
        category.name = json_data['name']
        db.session.commit()

        result = category_schema.dump(category)

        return jsonify({"message" : "Updated Successfully!", "data" : result})

    def delete(self):
        json_data = request.get_json(force=True)

        if not json_data or not 'id' in json_data:
            return {"error" : "Id not provided"}, 400
        
        deleted_row = Category.query.filter_by(id=json_data['id']).delete()

        db.session.commit()

        message = 'Deleted Successfully!' if deleted_row >0 else 'Failed to delete!'

        return jsonify({"message" : message})