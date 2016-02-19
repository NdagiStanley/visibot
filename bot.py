import os
import json
from flask import Flask
from flask_restful import Resource, Api, reqparse
from slackclient import SlackClient

app = Flask(__name__)
api = Api(app)

token = os.environ.get('SLACK_KEY')
sc = SlackClient(token)
print sc.api_call('api.test')


class RealName(Resource):
	def get(self):
		# return real_name from user id info from slack
		pass

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
			message = 'You have a visitor called {} at the gate.'.format(visitor_name)
		else:
			message = 'Hi! You have a visitor waiting for you.'

		# returns a string - to be converted to dict later. Then retrieve
		# channel ID
		string_resp = sc.api_call('im.open', user=user_id)
		dict_resp = json.loads(string_resp)
		channelID = dict_resp.get('channel').get('id')
		abc = sc.api_call(
			'chat.postMessage',
			as_user='true:',
			channel=channelID,
			text=message
		)
		return {'message': 'Notification sent'}, 200


api.add_resource(PostDM, '/send')


if __name__ == '__main__':
	app.run(debug=True)
