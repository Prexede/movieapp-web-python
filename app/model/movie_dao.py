from app.model.movie import Movie
from app.model.database import Database


class MovieDao:

  def get_all(self):
    conn = Database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, year FROM movie;")
    movies = []
    for row in cursor.fetchall():
      movies.append(Movie(row[0], row[1], row[2]))
    cursor.close()
    conn.close()

    return movies

  def add(self, movie):
    conn = Database.get_connection()
    cursor = conn.cursor()
    new_movie = (
        movie.name,
        movie.year,
    )
    cursor.execute("INSERT INTO movie (name, year) VALUES (?, ?);", new_movie)
    conn.commit()
    cursor.close()
    conn.close()

  def delete(self, iid):
    conn = Database.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movie WHERE id=?;", (iid, ))
    conn.commit()
    cursor.close()
    conn.close()

 #Funçao para buscar filme pelo ID
  def get(self, movie_id):
    conn = Database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, year FROM movie WHERE id = ?;",
                   (movie_id, ))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
      return Movie(row[0], row[1], row[2])
    return None
  
  #Função para atualizar filme
  def update(self, movie):
    conn = Database.get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE movie SET name = ?, year = ? WHERE id = ?;",
                   (movie.name, movie.year, movie.id))
    conn.commit()
    cursor.close()
    conn.close()
