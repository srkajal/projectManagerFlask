from flask_restful import Resource
from flask import request, jsonify
from Model import db, Comment, CommentSchema, Category

comments_schema = CommentSchema(many=True)
comment_schema = CommentSchema()

class CommentResource(Resource):
    def get(self):
        comments = Comment.query.all()
        updatedComments = []

        for comment1 in comments:
            newComment = {
                "id": comment1.id,
                "comment" : comment1.comment,
                "creation_date": comment1.creation_date,
                "category_id": comment1.category_id,
                "category_name": comment1.category.name
            }
            updatedComments.append(newComment)

        comments = comments_schema.dump(updatedComments)
        return {"status" : "success", "data" : comments}, 200

    def post(self):
        json_data = request.get_json(force=True)

        if not json_data or not 'category_id' in json_data or not 'comment' in json_data:
            return {"error" : "No input data provided"}, 400

        print(json_data)
        
        category = Category.query.filter_by(id=json_data['category_id']).first()

        if not category:
            return {'message': 'Category does not exists!'}, 400
        
        comment = Comment(
            comment = json_data['comment'],
            category_id = json_data['category_id']
        )

        db.session.add(comment)
        db.session.commit()

        result = comment_schema.dump(comment)

        return {"message" : "Saved successfully!", "data" : result}, 201

    def put(self):
        json_data = request.get_json(force=True)

        if not json_data or not 'category_id' in json_data or not 'id' in json_data or not 'comment' in json_data:
            return {"error" : "Id or category_id or comment input data not provided"}, 400
        
        category = Category.query.filter_by(id=json_data['id']).first()

        if not category:
            return {'message': 'Category doe not exists'}, 400
        
        comment = Comment.query.filter_by(id=json_data['id']).first()

        if not comment:
            return {'message': 'Comment doe not exists'}, 400

        comment.comment = json_data['comment']
        comment.category_id = json_data['category_id']
        
        db.session.commit()

        result = comment_schema.dump(comment)

        return jsonify({"message" : "Updated Successfully!", "data" : result})

    def delete(self):
        json_data = request.get_json(force=True)

        if not json_data or not 'id' in json_data:
            return {"error" : "Id not provided"}, 400
        
        deleted_row = Comment.query.filter_by(id=json_data['id']).delete()

        db.session.commit()

        message = 'Deleted Successfully!' if deleted_row >0 else 'Failed to delete!'

        return jsonify({"message" : message})