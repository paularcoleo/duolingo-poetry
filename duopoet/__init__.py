from flask import Flask, render_template, url_for, abort, request
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security import login_required, current_user

app = Flask(__name__)
app.config.from_object('duopoet.default_settings')

db = SQLAlchemy(app)
manager =  Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(threaded=True))

# Flask Security defined Models
from duopoet.models import Member, Role
# Custom Models
from duopoet.models import Fragment, Poem

user_datastore = SQLAlchemyUserDatastore(db, Member, Role)
Security = Security(app, user_datastore)

@app.route('/')
def home():
	return render_template('base.html')

@app.route('/ok')
@login_required
def test():
	return "ok, you loggin in now {0}".format(current_user.email)

@app.route('/add-fragments', methods=['POST', 'GET'])
def add_fragments():
	if request.method == "GET":
		return "ok let's go"
	else:
		return abort(404)
