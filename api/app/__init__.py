from flask import Flask
from flask_json import FlaskJSON
from flasgger import Swagger

'''initialized Flask application'''
app = Flask(__name__)
app.config['JSON_ADD_STATUS'] = False
app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "specs": [
        {
            "version": "1.0.0",
            "title": "AirBnB Clone Api v1",
            "endpoint": 'v1_spec',
            "route": '/spec',
			"description": 'AirBnB clone API documentation',
        }
    ]
}
Swagger(app)

'''initialized FlaskJSON with app'''
json = FlaskJSON(app)

'''Imports all views'''
from views import *
