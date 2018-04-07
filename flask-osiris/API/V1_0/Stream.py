import json
import uuid
from flaskapp import db, app
from flask import redirect, jsonify, abort, request, Response, send_file, send_from_directory, make_response, session
from sqlalchemy.dialects.postgresql import JSON
from Model.Stream_Model import Stream_Model
from Model.Device_Model import Device_Model
import datetime

BASE_URL = "www.osiris.com"

class Stream():

	@staticmethod
	def on_publish():
		parsed_json = request.get_json()
		stream_key = parsed_json["name"]

		stream = Stream_Model.query.filter(Stream_Model.id == stream_key).first()

		if stream is None:
			dict_local = {'message': "Stream does not exist."}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return Response(return_string, status=400, mimetype='application/json')

		stream.live_at = datetime.datetime.now()
		db.session.commit()

		device = Device_Model.query.join(Stream_Model, Stream_Model.device == Device_Model.id).filter(Stream_Model.id == stream_key).first()

		if device is None:
			dict_local = {'message': "No Device."}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return Response(return_string, status=400, mimetype='application/json')


		new_url = BASE_URL + "/device/" + device.id

		return redirect(new_url, code=200)


	@staticmethod
	def on_publish_done():
		return 'TODO'


	@staticmethod
	def create_stream():
		if 'user' in session.keys():

			parsed_json = request.get_json()
			device_id = parsed_json['device_id']

			device = Device_Model.query.filter(Device_Model.id == device_id).first()

			if device is None:
				dict_local = {'message': "No Device."}
				return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
				return Response(return_string, status=400, mimetype='application/json')

			id = str(uuid.uuid4())

			stream = Stream_Model(id, device_id)
			db.session.add(stream)
			db.session.commit()

			dict_local = {'stream_id': id}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return Response(return_string, status=200, mimetype='application/json')
		else:
			dict_local = {'message': "Auth error."}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return Response(return_string, status=400, mimetype='application/json')

	@staticmethod
	def get_device_streams():
		if 'user' in session.keys():
			parsed_json = request.get_json()
			device_id = parsed_json['device_id']

			device = Device_Model.query.filter(Device_Model.id == device_id).first()

			if device is None:
				dict_local = {'message': "No Device."}
				return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
				return Response(return_string, status=400, mimetype='application/json')


			streams = Stream_Model.query.filter(Stream_Model.device == device_id).all()

			array_local = []
			for stream in streams:
				dict_local = {}
				dict_local['id'] = stream.id
				dict_local['live_at'] = str(stream.live_at)
				array_local += [dict_local]

			return_string = json.dumps(array_local, sort_keys=True, indent=4, separators=(',', ': '))
			return Response(return_string, status=200, mimetype='application/json')
		else:
			dict_local = {'message': "Auth error."}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return Response(return_string, status=400, mimetype='application/json')




app.add_url_rule('/v1_0/on_publish', 'on_publish', Stream.on_publish, methods=['POST'])
app.add_url_rule('/v1_0/on_publish_done', 'on_publish_done', Stream.on_publish_done, methods=['POST'])
app.add_url_rule('/v1_0/create_stream', 'create_stream', Stream.create_stream, methods=['POST'])
app.add_url_rule('/v1_0/get_device_streams', 'get_device_streams', Stream.get_device_streams, methods=['POST'])


