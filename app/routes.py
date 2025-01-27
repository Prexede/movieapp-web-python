from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user
from app.model.user_dao import UserDao
from app.model.movie_dao import MovieDao
from app.model.movie import Movie
from app.model.user import User

userDAO = UserDao()
movieDAO = MovieDao()

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
  return render_template('index.html')


@bp.route('/login', methods=['POST'])
def login():
  user = userDAO.find(request.form['username'])
  if user is None:
    return render_template('index.html', error="Inexistent user.")

  if user.password != request.form['password']:
    return render_template('index.html', error="Incorrect password.")

  login_user(user)
  flash('You were successfully logged in')
  return redirect(url_for('main.main'))


@bp.route('/main')
@login_required
def main():
  return render_template('main.html')


@bp.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('main.index'))


@bp.route('/movie', methods=['GET', 'POST'])
@login_required
def movie():
  if request.method == "GET":
    return render_template('movie.html')
  elif request.method == "POST":
    movie = Movie(None, request.form['moviename_field'],
                  int(request.form['year_field']))
    movieDAO.add(movie)
    return redirect(url_for('main.main'))
  else:
    return redirect(url_for('main.main'))


@bp.route('/del_movie', methods=['GET'])
@login_required
def del_movie():
  iid = request.args.get('id')
  if iid:
    movieDAO.delete(iid)
    flash('Movie was removed!')
  return redirect(url_for('main.main'))


@bp.route('/movies')
@login_required
def movies():
  movies = []
  for m in movieDAO.get_all():
    movies.append({"id": m.id, "name": m.name, "year": m.year})
  return render_template('movies.html', movies=movies)


@bp.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    user_name = request.form.get('new_username')
    user_password = request.form.get('new_password')
    existing_user = userDAO.find(user_name)

    if existing_user:
      flash("O nome de usuário já existe. Por favor, escolha outro.", 'error')
      return render_template('register.html')

    try:
      new_user = User(user_name, user_password)
      userDAO.add(new_user)
      flash("Usuário registrado com sucesso. Por favor, faça o login.",
            'success')
      return redirect(url_for('main.index'))
    except Exception as e:
      flash(f"Ocorreu um erro ao registrar o usuário: {e}", 'error')
      return render_template('register.html')
  else:
    return render_template('register.html')


@bp.route('/edit_movie/<int:movie_id>', methods=['GET', 'POST'])
def edit_movie(movie_id):
  movie = movieDAO.get(movie_id)

  if request.method == 'POST':
    movie.name = request.form['movie_name']
    movie.year = request.form['movie_year']
    movieDAO.update(movie)
    flash('Movie updated successfully!')
    return redirect(url_for('main.movies'))
  else:
    return render_template('edit_movie.html', movie=movie)
