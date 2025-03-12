from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Movie Model with required fields
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    director = db.Column(db.String(100))
    year = db.Column(db.Integer)
    watched = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Integer)  # 1-5 stars
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Movie {self.title} ({self.year})>'

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    # Get all movies ordered by most recently added
    movies = Movie.query.order_by(Movie.added_at.desc()).all()
    return render_template('index.html', movies=movies)

@app.route('/add', methods=['POST'])
def add():
    # Get form data
    title = request.form.get('title')
    director = request.form.get('director')
    year = request.form.get('year')
    
    # Basic validation before adding to database
    if title:
        new_movie = Movie(
            title=title,
            director=director,
            year=int(year) if year else None
        )
        db.session.add(new_movie)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/toggle/<int:movie_id>')
def toggle(movie_id):
    # Toggle watched status
    movie = Movie.query.get_or_404(movie_id)
    movie.watched = not movie.watched
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/rate/<int:movie_id>/<int:rating>')
def rate(movie_id, rating):
    # Update movie rating
    movie = Movie.query.get_or_404(movie_id)
    movie.rating = rating
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:movie_id>')
def delete(movie_id):
    # Delete a movie from the database
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)