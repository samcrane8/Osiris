import json
import uuid
from Utility.Encryptor import Encryptor
from Utility.color_print import ColorPrint
from flaskapp import db, app
from flask import request, Response, send_file, send_from_directory, make_response, session
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

		stream.live_at = datetime.now()
		session.commit()

		url = BASE_URL + "/device/" + stream.device.id

		return redirect("http://www.example.com", code=200)


	@staticmethod
	def on_publish_done():
		return 'TODO'


app.add_url_rule('/on_publish', 'on_publish', Stream.on_publish, methods=['POST'])


