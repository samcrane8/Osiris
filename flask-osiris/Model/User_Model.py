import json
import uuid
from flaskapp import db, app
from sqlalchemy.dialects.postgresql import JSON
from flask import request, Response, send_file, send_from_directory
from Utility.color_print import ColorPrint
import datetime

class User_Model(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Text, primary_key=True)
    email = db.Column(db.Text)
    name = db.Column(db.Text)
    password = db.Column(db.Text)
    account_type = db.Column(db.Text)

    def __init__(self, id, name, password, email, account_type):
        self.id = id
        self.name = name
        self.password = password
        self.email = email
        #self.created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
        self.account_type = account_type

    def __repr__(self):
        return '<id {}>'.format(self.id)


    @staticmethod
    def authenticate_email_password(email, password):
        if not email or not password:
            return False
        user_info = User_Model.query.filter_by(email = email).first()
        if user_info is None:
                return None
        if user_info.password is not None:
                if user_info.password == password:
                        return user_info
        return None
