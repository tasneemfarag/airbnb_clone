# -*- coding: utf-8 -*-
from flask_json import as_json
from datetime import datetime
from app.models.base import db
from app import app
import re

'''allow only get request'''
@app.route('/', methods=['GET'])
@as_json
def index():
    '''get the current datetime in UTC and the current of the server'''
    data = {}
    data['status'] = 'OK'
    data['utc_time'] = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
    data['time'] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    return data

'''to open databse connection using db'''
@app.before_request
def _db_connect():
    db.connect()

'''to close databse connection using db'''
@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()

@app.errorhandler(404)
@as_json
def not_found(e):
    ''' return a JSON with code = 404 and msg = "not found"'''
    return {"code":404, "msg":"not found"}, 404

@app.errorhandler(500)
@as_json
def not_found(e):
    ''' return a JSON with code = 500 and msg = "server"'''
    return {"code":500, "msg":"server error"}, 500

def type_test(data, data_type):
    if data_type == int:
        try:
            int(data)
            return True
        except:
            return False
    elif data_type == float:
        try:
            float(data)
            return True
        except:
            return False
    elif data_type == bool:
        if data == 'True' or data == 'False':
            return True
        return False
    elif data_type == 'email':
        pattern = re.compile("^([A-z0-9\"“][\w-]*[+\.]?[\w-]+[\"”]{0,1}@[A-z0-9][\w-]*\.[\w]+\.?[\w]{0,3}\.?[\w]{0,3}\]{0,1})$")
        if pattern.match(data):
            return True
        return False
    elif data_type == 'string':
        if type_test(data, int):
            return False
        elif type_test(data, float):
            return False
        return True
