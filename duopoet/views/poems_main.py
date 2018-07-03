from flask import render_template

from duopoet import app
from duopoet.services import PoemService

ps = PoemService()

@app.route('/poems/', methods=['GET'])
def poems():
    poems = ps.get_most_recent(10)
    return render_template('poems_main.html', poems=poems)