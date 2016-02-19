import os
import json
import requests
from flask import Flask
from flask_restful import Resource, Api, reqparse
from slackclient import SlackClient

app = Flask(__name__)
api = Api(app)

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
        names = []
        for id in ids:
            for user in content:
                if id == user.get('id') and not user.get('deleted') and not user.get('is_bot'):  # noqa
                    names.append(
                        {
                            'id': id,
                            'name': user.get('real_name'),
                            'images': user.get('profile').get('image_48')
                        }
                    )
        return names

    def get(self):
        # return real_name from user id info from slack
        ids = self.user_ids()
        output = self.get_username(ids)
        return output


api.add_resource(RealName, '/names')


class PostDM(Resource):
    def post(self):
        # expect user_id and message data from the client
        parser = reqparse.RequestParser()
        parser.add_argument('user_id')
        parser.add_argument('visitor_name')
        # assign data from request to variables
        args = parser.parse_args()
        user_id = args.get('user_id')
        visitor_name = args.get('visitor_name')

        if visitor_name:
            message = 'You have a visitor called {} at the gate.'.format(
                visitor_name)
        else:
            message = 'Hi! You have a visitor waiting for you.'

        # returns a string - to be converted to dict later. Then retrieve
        # channel ID
        string_resp = sc.api_call('im.open', user=user_id)
        dict_resp = json.loads(string_resp)
        channelID = dict_resp.get('channel').get('id')
        sc.api_call(
            'chat.postMessage',
            as_user='true:',
            channel=channelID,
            text=message
        )
        return {'message': 'Notification sent'}, 200


api.add_resource(PostDM, '/send')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
