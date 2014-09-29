#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.login import login_required, login_user, current_user, logout_user
from flask import render_template, request, jsonify, make_response, Response, flash, redirect, session, url_for, g
from reminder.models import Base, User, Alias, Reminder
from reminder import config
from forms import LoginForm

from sqlalchemy import desc, and_
from sqlalchemy.orm import load_only

import json

from twilio.rest import TwilioRestClient

import twilio.twiml
import random

app = Flask(__name__)
app.config.from_object(config)

lm = LoginManager()
lm.init_app(app)

db = SQLAlchemy(app)
db.Model = Base

@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(id):
	return db.session.query(User).get(int(id))

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('dashboard'))

	form = LoginForm() if request.method == 'POST' else LoginForm(request.args)
	if form.validate_on_submit():

		user = db.session.query(User).filter_by(username=form.username.data).filter_by(password=form.pin.data).first()
		if user is None:
			flash('User does not exist, please register.')
			return redirect(url_for('welcome'))

		login_user(user)
		flash(('Logged in successfully.'))
		return redirect(url_for('dashboard'))
	return render_template('login.html', form=form)
	
@app.route('/dashboard')
@login_required
def dashboard():
	reminders = db.session.query(Reminder).filter_by(owner_id=g.user.id)
	return render_template('dashboard.html', reminders=reminders)

@app.route('/welcome', methods=['GET'])
def welcome():	
	return render_template('welcome.html')


@app.route('/welcome', methods=['POST'])
def signup():
	name = request.form['username']
	phone = request.form['phone']
	pin = request.form['pin']

	try:
		user_id = db.session.query(User).filter_by(username=name).first().id
		print "error"
		return jsonify(error="username already in use")
	except AttributeError,e:
		new_user = User(username=name, password=pin, phone=phone)
		db.session.add(new_user)
		db.session.commit()
		return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/_add_reminder', methods=['POST'])
def add_reminder():
	owner_id = g.user.id
	description = request.form['description']

	print g.user.reminders
	new_reminder = Reminder(owner_id=owner_id, description=description)
	db.session.add(new_reminder)
	db.session.commit()

	return jsonify(result='success')


@app.route('/_receive_text', methods=['GET', 'POST'])
def receive_text():
	resp = twilio.twiml.Response()
	#resp.message("Hello, Mobile Monkey")
	resp.redirect("http://enigmatic-falls-5410.herokuapp.com/_send_text")
	return str(resp)

@app.route('/_send_text', methods=['POST'])
def send_text():

	#request.form['body']

	ACCOUNT_SID = "ACf2b361a5b8be85173d9db27f45cfb5d2" 
	AUTH_TOKEN = "4b6edb9fb0efffc0fa1a3c293b8e16c4" 
 
	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
 	
 	try:
		user = db.session.query(User).filter_by(username=request.form['Body']).first()

		emptyList = []
		reminder = db.session.query(Reminder).filter_by(owner_id=user.id)

		for item in reminder:
			emptyList.append(item)

		selected = random.choice(emptyList)

		remindString = "Don't forget! " + selected.description
		client.messages.create(
			to=user.phone, 
			from_="+14406385597", 
			body=remindString,  
		)
	except:
		client.messages.create(
			to=request.form['From'],
			from_="+14406385597",
			body="Sorry, the user you tried to remind doesn't exist yet :(",
		)


# Example of ajax route that returns JSON
@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)