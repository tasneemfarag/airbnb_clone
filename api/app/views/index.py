from flask_json import as_json
from datetime import datetime
from app.models.base import db
from app import app

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
def before_request():
    db.database.connect()

'''to close databse connection using db'''
def after_request():
    db.database.close()

@app.errorhandler(404)
@as_json
def not_found(error):
    ''' return a JSON with code = 404 and msg = "not found"'''
    return {"code":404, "msg":"not found"}, 404
