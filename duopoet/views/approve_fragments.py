from flask import request, flash, abort, render_template, redirect, url_for

from duopoet import app
from duopoet.services import FragmentService
from duopoet.forms import ApproveFragmentsForm

fs = FragmentService()

@app.route('/fragments/approve', methods=['GET', 'POST'])
def approve_fragments():
	if request.method == 'GET':
		fragment = fs.get_unapproved_fragments(1)
		return render_template('approve_fragments.html', fragment=fragment, form=ApproveFragmentsForm())

	elif request.method == 'POST':
		submit = request.form.get('submit')
		delete = request.form.get('delete')
		fragment_id = int(request.form.get('fragment_id'))
		if submit and not delete:
			fragment_text = request.form.get('fragment_text')
			if fs.is_unique(fragment_text, id=fragment_id):
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