import json
import uuid
from flaskapp import db, app
from sqlalchemy.dialects.postgresql import JSON
from flask import request, Response, send_file, send_from_directory
from Utility.color_print import ColorPrint
import datetime

class Device_Model(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Text, primary_key=True)
    owner = db.Column(db.Text, db.ForeignKey("users.id"))
    location = db.Column(db.JSON)
    stream_url = db.Column(db.Text, default="")
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, id, owner, location):
        self.id = id
        self.owner = owner
        self.location = location

    def __repr__(self):
        return '<id {}>'.format(self.id)
