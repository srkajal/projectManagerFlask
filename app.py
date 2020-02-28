from flask import Blueprint
from flask_restful import Api
from resources.Hello import Hello
from resources.Category import CategoryResource
from resources.Comment import CommentResource
from resources.ParentTask import ParentTaskResource
from resources.User import UserResource
from resources.Project import ProjectResource
from resources.Task import TaskResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

#Route
api.add_resource(Hello, "/hello")
api.add_resource(CategoryResource, "/category")
api.add_resource(CommentResource, "/comment")
api.add_resource(ParentTaskResource, "/parent")
api.add_resource(UserResource, "/user")
api.add_resource(ProjectResource, "/project")
api.add_resource(TaskResource, "/task")