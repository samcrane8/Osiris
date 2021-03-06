import json
import uuid
from Utility.Encryptor import Encryptor
from Utility.color_print import ColorPrint
from flaskapp import db, app
from flask import request, Response, send_file, send_from_directory, make_response, session
from sqlalchemy.dialects.postgresql import JSON
from Model.User_Model import User_Model
import datetime
import hashlib

class User():

	@staticmethod
	def isLoggedIn():
		return make_response(str('user' in session.keys()))

	@staticmethod
	def login():

		parsed_json = request.get_json()
		if "email" not in parsed_json.keys():
			dict_local = {'message': "No email attribute."}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return Response(return_string, status=400, mimetype='application/json')
		email = parsed_json["email"]

		if "password" not in parsed_json.keys():
			dict_local = {'message': "No password attribute."}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return Response(return_string, status=400, mimetype='application/json')
		password = parsed_json["password"]
		password = str(hashlib.sha256(password.encode()).hexdigest())

		user_info = User_Model.authenticate_email_password(email, password)
		if user_info is not None:
			#then this data is good, and we're in.

			user = {'id': user_info.id, 'name': user_info.name, 'email' : email, 'password' : password}
			
			if 'user' in session.keys():
				dict_local = {'message': "already logged in"}
			else:
				session['user'] = user
				session.modified=True
				dict_local = {'message': "Logged in successfully."}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return Response(return_string, status=200, mimetype='application/json')
		else:
			#not a good cookie and no login.
			dict_local = {'message': "Password or username is wrong."}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return Response(return_string, status=400, mimetype='application/json')


	@staticmethod
	def logoff():
		if 'user' not in session.keys():
			dict_local = {'code': 31, 'message': "User not logged in anyways."}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string
		else:
			session.pop('user', None)
			session.modified = True
			dict_local = {'code': 200}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string


	@staticmethod
	def list_all_users():
		if 'user' in session.keys():
			user = session['user']
			if User_Model.query.filter_by(id = user["id"]).first().account_type == "admin":
				db_user_devices = User_Model.query.all()
				return_json_list = []
				for report in db_user_devices:
					dict_local = {'id': report.id,
													'name': report.name,
													'email': report.email,
													'password' : report.password,
													'created_at': str(report.created_at),
													'account_type': report.account_type}

					return_json_list.append(dict_local)
				return_string = json.dumps(return_json_list, sort_keys=True, indent=4, separators=(',', ': '))
				return return_string
			else:
				dict_local = {'code': 37, 'message': "Permission error " + user["email"]}
				return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
				return return_string
		else:
			dict_local = {'code': 31, 'message': "auth error"}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string

	@staticmethod
	def register_user():
		parsed_json = request.get_json()
		email = parsed_json["email"]
		password = parsed_json["password"]
		password = str(hashlib.sha256(password.encode()).hexdigest())
		name = parsed_json["name"]
		account_type = 'operator'

		if User_Model.query.filter_by(email = email).first() is None:
			id = str(uuid.uuid4())
			user = User_Model(id, name, password, email, account_type)
			db.session.add(user)
			db.session.commit()

			return_json = {'code': 200}
			return_string = json.dumps(return_json, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string
		else:
			dict_local = {'message': "Email already taken."}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return Response(return_string, status=400, mimetype='application/json')


	@staticmethod
	def update_user_info():
		if 'user' in session.keys():
			user = session['user']
			parsed_json = request.get_json()
			user_info = User_Model.query.filter_by(id = user["id"]).first()

			if 'email' in parsed_json:
				user_info.email = parsed_json['email']
			if 'password' in parsed_json:
				user_info.password = parsed_json['password']
			if 'name' in parsed_json:
				user_info.name = parsed_json['name']

			db.session.commit()

			return_dict = {'code': 200}
			return_string = json.dumps(return_dict, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string
		else:
			dict_local = {'code': 31, 'message': "auth error"}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string

	@staticmethod
	def get_user_info():
		if 'user' in session.keys():
			user = session['user']
			user_info = User_Model.query.filter_by(id = user["id"]).first()

			return_dict = {
				'email': user_info.email,
				'name': user_info.name,
				'created_at': str(user_info.created_at),
				'id': user['id']
			}

			return_string = json.dumps(return_dict, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string
		else:
			dict_local = {'code': 31, 'message': "auth error"}
			return_string = json.dumps(dict_local, sort_keys=True, indent=4, separators=(',', ': '))
			return return_string

app.add_url_rule('/v1_0/isLoggedIn', '/v1_0/isLoggedIn', User.isLoggedIn, methods=['GET'])
app.add_url_rule('/v1_0/login', '/v1_0/login', User.login, methods=['POST'])
app.add_url_rule('/v1_0/logoff', '/v1_0/logoff', User.logoff, methods=['GET'])
app.add_url_rule('/v1_0/list_all_users', '/v1_0/list_all_users', User.list_all_users, methods=['GET'])
app.add_url_rule('/v1_0/register_user', '/v1_0/register_user', User.register_user, methods=['POST'])
app.add_url_rule('/v1_0/get_user_info', '/v1_0/get_user_info', User.get_user_info, methods=['GET'])
app.add_url_rule('/v1_0/update_user_info', '/v1_0/update_user_info', User.update_user_info, methods=['POST'])
