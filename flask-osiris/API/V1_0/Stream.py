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

encryptor = Encryptor()
seconds_in_hour = 60*60
session_inactivity_timeout = datetime.timedelta(0, seconds_in_hour * 2)

BASE_URL = ""

class Stream():

	@staticmethod
	def on_publish():
		parsed_json = request.get_json()
		stream_key = parsed_json["name"]

		stream = Stream_Model.query.filter(Stream_Model.id == stream_key).first()

		if stream is None:
			abort(404) # Stream doesn't exist.

		stream.live_at = datetime.datetime.now()
		session.commit()

		device = Device_Model.query.join(Stream_Model, Stream_Model.device == Device_Model.id).filter(Stream_Model.id == stream_key).first()

		if device is None:
			raise InvalidUsage('This view is gone', status_code=500)

		new_url = BASE_URL + "/device/" + stream.device.id

		return redirect(new_url, code=200)


	@staticmethod
	def on_publish_done():
		return 'TODO'


	@staticmethod
	def create_stream():
		if 'user' in session.keys():
			
			
		else:
			dict_local = {'message': "Auth error."}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return Response(return_string, status=500, mimetype='application/json')



app.add_url_rule('/on_publish', 'on_publish', Stream.on_publish, methods=['POST'])


