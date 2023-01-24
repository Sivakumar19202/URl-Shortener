from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import random, string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.String(8), primary_key=True)
    original_url = db.Column(db.String)

    def __init__(self, original_url):
        self.id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        self.original_url = original_url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        if not original_url.startswith('http'):
            original_url = 'http://' + original_url
        url = URL(original_url)
        db.session.add(url)
        db.session.commit()
        short_url = request.host_url + url.id
        return render_template('index.html', short_url=short_url)
    return render_template('index.html')

@app.route('/<short_url>')
def redirect_url(short_url):
    url = URL.query.get(short_url)
    if url:
        return redirect(url.original_url)
    else:
        return 'Invalid URL'

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)