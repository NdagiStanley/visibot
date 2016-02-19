from flask import Flask
from flask_restful import Resource, Api
from slackclient import SlackClient

app = Flask(__name__)
api = Api(app)


class RealName(Resource):
    def get(self):
        # return real_name from user id info from slack
        pass

api.add_resource(RealName, '/names')


class PostDM(Resource):
    def post(self):
        # send dm to user in the request info

        pass

api.add_resource(PostDM, '/send')


if __name__ == '__main__':
    app.run(debug=True)
