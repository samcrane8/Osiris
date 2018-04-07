import json
import uuid
from flaskapp import db, app
from sqlalchemy.dialects.postgresql import JSON
from flask import request, Response, send_file, send_from_directory
from Utility.color_print import ColorPrint
import datetime

class Stream_Model(db.Model):
    __tablename__ = 'streams'
    id = db.Column(db.Text, primary_key=True)
    device = db.Column(db.Text, db.ForeignKey("devices.id"))
    live_at = db.Column(db.DateTime)

    def __init__(self, id, device):
        self.id = id
        self.device = device

    def __repr__(self):
        return '<id {}>'.format(self.id)
