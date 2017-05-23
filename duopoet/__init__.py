from flask import Flask, render_template, url_for, abort, request, jsonify, flash, redirect
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

from duopoet.forms import AddFragmentsForm
from duopoet.services import FragmentService, PoemService

fs = FragmentService()
ps = PoemService()

@app.route('/')
def home():
	return render_template('base.html')

@app.route('/fragments/add', methods=['GET', 'POST'])
def add_fragments():
	if request.method == 'GET':
		return render_template('add_fragments.html', form=AddFragmentsForm())
	elif request.method == 'POST':
		fragments = request.form.get('fragments').splitlines()
		date = datetime.utcnow().date()
		exists = []
		needs_redo = []
		for fragment in fragments:
			if '/' in fragment or "'" in fragment:
				needs_redo.append(fragment)
				continue
			if fs.is_unique(fragment):
				if fragment[-1] not in ['.', '?', '!']:
					fragment += '.' 
				fs.create(text=fragment, date_uploaded=date)
			else:
				exists.append(fragment)
		if exists:
			flash('{} Fragments already existed, and were not added.'.format(len(exists)))
		if needs_redo:
			flash('{} fragments need to be redone, because they have slashes or apostrophes.'.format(len(needs_redo)), Markup(needs_redo))
			return redirect(url_for('add_fragments'))
		return jsonify(fragments), 200
	else:
		abort(404)

@app.route('/poems/random')
@app.route('/poems/random/<int:n>', methods=['GET', 'POST'])
def poems_main(n=None):
	if n is None:
		n = random.randint(1,5)
	if n > 5:
		fragments = ['Sorry, max 5 sentences are allowed in a poem. ¯\_(ツ)_/¯']
		fragment_order = None
	else:
		fragments = fs.get_random_fragments(n)
		fragment_order = [fragment.id for fragment in fragments]
		fragments = [fragment.text for fragment in fragments]
	return render_template('poems.html', fragments=fragments, fragment_order=fragment_order)
