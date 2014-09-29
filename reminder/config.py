import os
PWD = os.path.abspath(os.curdir)

DEBUG=True
SQLALCHEMY_DATABASE_URI = 'postgres://PhilipHouse:house@localhost/reminder'
SECRET_KEY = 'thisissecret'
CSRF_ENABLED = True
SESSION_PROTECTION = 'strong'
