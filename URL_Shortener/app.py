from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Url
import string
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'randomsecretkey'
db.init_app(app)

# Generate a random short URL
def generate_short_id(num_of_chars):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=num_of_chars))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        if not original_url:
            flash('The URL is required!', 'danger')
            return redirect(url_for('index'))
        
        existing_url = Url.query.filter_by(original_url=original_url).first()
        if existing_url:
            return render_template('short_url.html', short_url=existing_url.short_url)

        short_url = generate_short_id(6)
        new_url = Url(original_url=original_url, short_url=short_url)
        db.session.add(new_url)
        db.session.commit()
        return render_template('short_url.html', short_url=short_url)

    return render_template('index.html')

@app.route('/<short_url>')
def redirect_to_url(short_url):
    url = Url.query.filter_by(short_url=short_url).first_or_404()
    return redirect(url.original_url)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
