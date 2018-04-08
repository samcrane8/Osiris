import json
import uuid
from Utility.Encryptor import Encryptor
from Utility.color_print import ColorPrint
from flaskapp import db, app
from flask import jsonify, abort, request, Response, send_file, send_from_directory, make_response, session
from sqlalchemy.dialects.postgresql import JSON
from Model.Stream_Model import Stream_Model
from Model.Device_Model import Device_Model
import datetime

BASE_URL = ""

class Device():

	@staticmethod
	def register_device():
		if 'user' in session.keys():
			user = session['user']
			parsed_json = request.get_json()
			owner = user["id"]
			id = str(uuid.uuid4())
			location = parsed_json["location"]
			stream_url = parsed_json["stream_url"]

			device = Device_Model(id, owner, location, stream_url)
			db.session.add(device)
			db.session.commit()

			dict_local = {'id': id}

			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string
		else:
			dict_local = {'message': "Auth error."}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return Response(return_string, status=400, mimetype='application/json')

	@staticmethod
	def delete_device():
		if 'user' in session.keys():

			user = session['user']
			email = user['email']
			parsed_json = request.get_json()

			id = parsed_json["id"]

			drone = Device_Model.query.filter_by(id=id).first()
			if drone is None:
				dict_local = {'code': 31, 'message': "Bad drone id."}
				return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
				return return_string
			db.session.delete(drone)
			db.session.commit()

			dict_local = {'id': id}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string
		else:
			dict_local = {'message': "Auth error."}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return Response(return_string, status=500, mimetype='application/json')

	@staticmethod
	def get_user_devices():
		if 'user' in session.keys():

			user = session['user']
			email = user['email']
			id = user['id']

			devices = Device_Model.query.filter_by(owner=id).all()

			array_local = []

			for device in devices:
				dict_local = {}
				dict_local['id'] = device.id
				dict_local['location'] = device.location
				dict_local['stream_url'] = device.stream_url

				array_local += [dict_local]

			
			return_string = json.dumps(array_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string
		else:
			dict_local = {'message': "Auth error."}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return Response(return_string, status=400, mimetype='application/json')


app.add_url_rule('/v1_0/register_device', '/v1_0/register_device', Device.register_device, methods=['POST'])
app.add_url_rule('/v1_0/delete_device', '/v1_0/delete_device', Device.delete_device, methods=['POST'])
app.add_url_rule('/v1_0/get_user_devices', '/v1_0/get_user_devices', Device.get_user_devices, methods=['GET'])


