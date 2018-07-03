from flask import request, render_template, jsonify, flash, abort

from duopoet import app
from duopoet.services import FragmentService
from duopoet.forms import AddFragmentsForm

from datetime import datetime

fs = FragmentService()

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