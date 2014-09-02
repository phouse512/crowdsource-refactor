#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import render_template, request, jsonify, make_response, Response
from reminder.models import Base, User, Alias, Reminder
from reminder import config

from sqlalchemy import desc, and_
from sqlalchemy.orm import load_only

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)
db.Model = Base

@app.route('/welcome')
def welcome():


	
	return render_template('welcome.html')


# Example of ajax route that returns JSON
@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)