from flask import Flask, render_template, url_for, abort
from flask import request, jsonify, flash, redirect
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from markupsafe import Markup

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
	return render_template('base.html')
