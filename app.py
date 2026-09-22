from flask import Flask, g, render_template
import sqlite3


DATABASE = 'database.db'




#initialise the Flask app
app = Flask(__name__)  


def get_db():
   # Connects to the SQLite database if not already connected.
   # Stores the active connection in Flask's global context object g.
   db = getattr(g, '_database', None)
   if db is None:
       db = g._database = sqlite3.connect(DATABASE)
   return db


@app.teardown_appcontext
def close_connection(exception):
   # Automatically closes the database connection when the app context ends.
   # Receives an optional exception argument if an error occurs during the request.
   db = getattr(g, '_database', None)
   if db is not None:
       db.close()




def query_db(query, args=(), one=False):
   # Executes a parameterized SQL query safely against the database.
   # Fetches all results or returns only the first item if 'one' is True.
   cur = get_db().execute(query, args)
   rv = cur.fetchall()
   cur.close()
   return (rv[0] if rv else None) if one else rv





# route for the home page
@app.route('/')
def home():
   # Renders the home page with a full list of games and their studios.
   # Executes a JOIN query to combine game and studio records.
   sql="""
   SELECT * FROM game
   JOIN studio ON game.studioid = studio.studioid;"""


   results = query_db(sql)
   return render_template('home.html', results=results)


# game page route
@app.route("/game/<int:gameid>")
def game(gameid):
    # Displays the detailed page for a specific game by its ID.
    # Returns 404 page if no matching game is found.
    spl = """SELECT * FROM game JOIN studio ON game.studioid = studio.studioid
    WHERE game.gameid = ?;"""
    result = query_db(spl, (gameid,), True)
    
    if result:
        return render_template('game.html', game=result)
    return render_template('404.html'), 404

# route for the game page
@app.route('/games')
def gamepage():
    # Renders the main games listing page for users.
    # Retrieves all games along with their corresponding studio information.
    sql = """SELECT * FROM game
             JOIN studio ON game.studioid = studio.studioid;"""
    results = query_db(sql)
    return render_template('gamepage.html', results=results)

# route for the category 
@app.route('/category/<int:id>')
def cartegory(id):
    # Filters games by their classification category ID.
    # Returns 404 page if the category has no games or does not exist.
    sql = """SELECT * FROM game
             JOIN studio ON game.studioid = studio.studioid
             WHERE game.classificationid = ?"""
    results = query_db(sql, (id,))
    
    if results:
        return render_template('gamepage.html', results=results)
    return render_template('404.html'), 404

# route for the news page
@app.route('/gamenews')
def gamenews():
    # Displays the main news overview page containing all news articles.
    # Queries the gamenews table to fetch all news records.
    sql = """SELECT * FROM gamenews"""
    results = query_db(sql)
    return render_template('gamenews.html', results=results)

# route for the each news own page
@app.route('/newspage/<int:id>')
def newspage(id):
    # Fetches and renders a single news article page by article ID.
    # Returns 404 page if no matching article is found in the database.
    sql = """SELECT * FROM gamenews
     WHERE gamenews.articleid = ?"""
    results = query_db(sql, (id,))
    
    if results:
        return render_template('newspage.html', gamenews=results[0])
    return render_template('404.html'), 404

# custom error handler for 404 errors
@app.errorhandler(404)
def page_not_found(e):
    # Handles invalid URLs or missing pages across the application.
    # Renders the 404.html error template with a 404 status code.
    return render_template('404.html'), 404

# explicit route for 404 page
@app.route('/404')
def error_404():
    # Renders the 404 error page directly if accessed via /404 URL.
    # Returns the 404.html template with a 404 status code.
    return render_template('404.html'), 404


if __name__ == '__main__':   
   app.run(debug=True)