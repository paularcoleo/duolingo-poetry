from flask import render_template, request, redirect, url_for

from duopoet import app
from duopoet.forms import PoemForm
from duopoet.services import FragmentService, PoemService

import random

fs = FragmentService()
ps = PoemService()

@app.route('/poems/random', methods=['GET', 'POST'])
@app.route('/poems/random/<int:n>', methods=['GET', 'POST'])
def generate_poems(n=None):
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