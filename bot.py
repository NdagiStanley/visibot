<<<<<<< HEAD
import os
import json
import requests
from flask import Flask
from flask_restful import Resource, Api, reqparse
=======
from flask import Flask
from flask_restful import Resource, Api
>>>>>>> pre_bot
from slackclient import SlackClient

app = Flask(__name__)
api = Api(app)

<<<<<<< HEAD
token = os.environ.get('SLACK_KEY')
sc = SlackClient(token)
print sc.api_call('api.test')


class RealName(Resource):
    def user_ids(self):
        r = requests.get(
            'https://slack.com/api/groups.list?token={}'.format(token))
        content = r.json()
        return content.get('groups')[0].get('members')

    def get_username(self, ids):
        r = requests.get(
            'https://slack.com/api/users.list?token={}'.format(token))
        content = r.json().get('members')
        names = [{
            'id': id,
            'name': user.get('real_name'),
            'images': user.get('profile').get('image_48')
        } for id in ids for user in content if (id == user.get('id') and
                                                not user.get('deleted') and
                                                not user.get('is_bot'))]
        return names

    def get(self):
        # return real_name from user id info from slack
        ids = self.user_ids()
        output = self.get_username(ids)
        return output


api.add_resource(RealName, '/names')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
=======

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
>>>>>>> pre_bot
