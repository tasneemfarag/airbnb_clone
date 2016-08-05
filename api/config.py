from os import environ

'''script  to define some variables of your RestAPI application depending of the environment variable AIRBNB_ENV'''

DATABASE = {}
DATABASE['host'] = '158.69.91.92'
DATABASE['port'] = 3306
DATABASE['charset'] = 'utf8'
if environ.get('AIRBNB_ENV') == 'production':
    ''' Production specific variables '''
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = 3000
    DATABASE['user'] = 'airbnb_user_prod'
    DATABASE['database'] = 'airbnb_prod'
    DATABASE['password'] = environ.get('AIRBNB_DATABASE_PWD_PROD')
elif environ.get('AIRBNB_ENV') == 'test':
    ''' Test specific variables '''
    DEBUG = False
    HOST = 'localhost'
    PORT = 5555
    DATABASE['user'] = 'airbnb_user_test'
    DATABASE['database'] = 'airbnb_test'
    DATABASE['password'] = environ.get('AIRBNB_DATABASE_PWD_TEST')
else:
    ''' Development specific variables '''
    DEBUG = True
    HOST = 'localhost'
    PORT = 3333
    DATABASE['user'] = 'airbnb_user_dev'
    DATABASE['database'] = 'airbnb_dev'
    DATABASE['password'] = environ.get('AIRBNB_DATABASE_PWD_DEV')
