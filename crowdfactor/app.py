#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import render_template, request, jsonify, make_response, Response, flash, redirect, session, url_for, g
from crowdfactor.models import Base, User, Alias, Reminder
from crowdfactor import config


from sqlalchemy import desc, and_
from sqlalchemy.orm import load_only

import json

app = Flask(__name__)
app.config.from_object(config)

#lm = LoginManager()
#lm.init_app(app)

db = SQLAlchemy(app)
db.Model = Base

	
@app.route('/leader')
def dashboard():
	return render_template('dashboard.html')

@app.route('/worker/1')
def worker1():
	return render_template('worker1.html')

@app.route('/welcome', methods=['GET'])
def welcome():	
	return render_template('welcome.html')