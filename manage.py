from flask.ext.script import Manager

from crowdfactor.app import app, db


manager = Manager(app)
app.config['DEBUG'] = True 

@manager.command
def create_tables():
	"Create relational database tables."
	db.create_all()

if __name__ == '__main__':
	manager.run()