from flask import Flask, url_for, send_from_directory, redirect
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
import random

app = Flask(__name__)
app.config.from_object('duopoet.default_settings')

db = SQLAlchemy(app)
manager =  Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(threaded=True))

import duopoet.views

@app.route('/')
def home():
	return redirect(url_for('poems'))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', filename='img/duopoet.png')
