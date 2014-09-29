from datetime import datetime
import os
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship, synonym, backref

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

""" User """
class User(Base):
	__tablename__ = 'reminder_user'

	id = Column(Integer, primary_key=True)
	username = Column(String(200))
	password = Column(String(100))
	phone = Column(String(10))

	def __init__(self, username, password, phone):
		self.username = username
		self.password = password
		self.phone = phone

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return '<User %r>' % self.username

""" Aliases """
class Alias(Base):
	__tablename__ = 'alias'

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('reminder_user.id'))
	user = relationship("User", backref=backref('aliases', order_by=id))
	alias_name = Column(String(50))

	def __init__(self, user_id, alias):
		self.user_id = user_id
		self.alias_name = alias

	def __repr__(self):
		return '<Alias %r>' % self.alias_name

""" Reminders """ 
class Reminder(Base):
	__tablename__ = 'reminder'

	id = Column(Integer, primary_key=True)
	owner_id = Column(Integer, ForeignKey('reminder_user.id'))
	owner = relationship("User", backref=backref('reminders', order_by=id))
	description = Column(String(200))

	def __init__(self, owner_id, description):
		self.owner_id = owner_id
		self.description = description

	def __repr__(self):
		return '<Reminder %r>' % self.description

if __name__ == '__main__':
	from datetime import timedelta

	from sqlalchemy import create_engine
	from sqlalchemy.orm import sessionmaker

	PWD = os.path.abspath(os.curdir)

	engine = create_engine('postgres://PhilipHouse:house@localhost/reminder', echo=True)

	Base.metadata.create_all(engine)
	Session = sessionmaker(bind=engine)
	session = Session()
