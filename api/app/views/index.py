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
