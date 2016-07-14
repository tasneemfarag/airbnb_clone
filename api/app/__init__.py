import os
from flask import Flask, request
from flask_json import FlaskJSON
import json

'''initialized Flask application'''
app = Flask(__name__)
app.config['JSON_ADD_STATUS'] = False

'''initialized FlaskJSON with app'''
json = FlaskJSON(app)
