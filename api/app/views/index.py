from flask import Flask
from flask_json import FlaskJSON
from datetime import datetime
from app.models.base import db
from app import app

'''allow only get request'''
@app.route('/', methods=['GET'])
def index():
    '''get the current datetime in UTC and the current of the server'''
    return json_response(status="OK", utc_time=datetime.utcnow().strftime("%m/%d/%y %H:%M:%S"), time=datetime.now().strftime("%m/%d/%y %H:%M:%S"))

'''to open databse connection using db'''
def before_request():
    db.database.connect()

'''to close databse connection using db'''
def after_request():
    db.database.close()

@app.errorhandler(404)
def not_found(error):
    ''' return a JSON with code = 404 and msg = "not found"'''
    return json_response(code=404, msg="not found")
