from flask import render_template

from duopoet import app

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')