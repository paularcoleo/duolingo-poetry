from flask import render_template, abort

from duopoet import app
from duopoet.services import PoemService

ps = PoemService()

@app.route('/poems/<id>', methods=['GET'])
def poem_detail(id):
    poem = ps.get(id)
    if poem is not None:
        return render_template('poems_detail.html', poem=poem)
    else:
        abort(404)