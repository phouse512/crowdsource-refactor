import os
PWD = os.path.abspath(os.curdir)

DEBUG=True
SQLALCHEMY_DATABASE_URI = 'postgres://qiyyulwagfkvzt:j_k8ydtSIEny7mwA87mCj68d9o@ec2-54-83-204-104.compute-1.amazonaws.com:5432/d9dppr2muk5dct'
SECRET_KEY = 'thisissecret'
CSRF_ENABLED = True
SESSION_PROTECTION = 'strong'
