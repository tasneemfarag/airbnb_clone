from app import app
from config import HOST, PORT, DEBUG

'''this code will run only if this file run directly not from another file'''
if __name__ == '__main__' :
    app.run(host=HOST, port=PORT, debug=DEBUG)
