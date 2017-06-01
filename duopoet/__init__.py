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

from duopoet.forms import AddFragmentsForm, ApproveFragmentsForm
from duopoet.forms import PoemForm
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
		for fragment in fragments:
			if fs.is_unique(fragment):
				if fragment[-1] in ('.', ','):
					fragment=fragment[:-1]
				fs.create(text=fragment.lower(), date_uploaded=date)
			else:
				exists.append(fragment)
		if exists:
			flash('{} Fragments already existed, and were not added.'.format(
				len(exists)))
		return jsonify(fragments), 200
	else:
		abort(404)

@app.route('/fragments/approve', methods=['GET', 'POST'])
def approve_fragments():
	form = ApproveFragmentsForm()
	if request.method == 'GET':
		fragment = fs.get_unapproved_fragments(1)
		return render_template('approve_fragments.html', fragment=fragment, form=form)

	elif request.method == 'POST':
		submit = request.form.get('submit')
		delete = request.form.get('delete')
		fragment_id = request.form.get('fragment_id')
		if submit and not delete:
			fragment_text = request.form.get('fragment_text')
			if fs.is_unique(fragment_text):
				fragment = fs.get(fragment_id)
				fragment = fs.update(fragment, text=fragment_text)
				fragment = fs.approve(fragment)
				flash('Fragment Approved: {}'.format(fragment.text), 'success')
				return redirect(url_for('approve_fragments'))
			else:

				fragment = fs.get(fragment_id)
				fs.delete(fragment)
				flash('Revised Fragment Conflicted with existing fragment and is now Deleted.', 'error')
				return redirect(url_for('approve_fragments'))
		elif delete and not submit:
			fragment = fs.get(fragment_id)
			fs.delete(fragment)
			flash('Fragment Deleted.')
			return redirect(url_for('approve_fragments'), 'warning')
		else:
			abort(404)



@app.route('/poems/random', methods=['GET', 'POST'])
@app.route('/poems/random/<int:n>', methods=['GET', 'POST'])
def poems_main(n=None):
    if request.method == 'GET':
    	if n is None:
    		n = random.randint(2,5)
    	if n > 5:
    		fragments = ['Sorry, max 5 sentences are allowed in a poem.']
    		fragment_order = None
    	else:
    		fragments = fs.get_random_fragments(n)
    		fragment_order = ','.join([str(fragment.id) for fragment in fragments])
    		fragments = [fragment.text for fragment in fragments]
    	return render_template('poems_random.html', fragments=fragments,
    		fragment_order=fragment_order, form=PoemForm())
    elif request.method == 'POST':
        fragment_order = request.form.get('fragment_order')
        if fragment_order is not None:
            fragment_ids = [int(frag) for frag in fragment_order.split(',')]
            fragments = fs.get_all(fragment_ids)
            poem = ps.create(fragments, fragment_order)

            return redirect(url_for('poem_detail', id=poem.id))


@app.route('/poems/<id>', methods=['GET'])
def poem_detail(id):
    poem = ps.get(id)
    if poem is not None:
        return render_template('poems_detail.html', poem=poem)
    else:
        abort(404)


@app.route('/poems/', methods=['GET'])
def poems():
    poems = ps.get_most_recent(10)
    return render_template('poems_main.html', poems=poems)