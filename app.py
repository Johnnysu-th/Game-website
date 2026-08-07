from flask import Flask, g, render_template
import sqlite3


DATABASE = 'database.db'




#initialise the Flask app
app = Flask(__name__)  


def get_db():
   db = getattr(g, '_database', None)
   if db is None:
       db = g._database = sqlite3.connect(DATABASE)
   return db


@app.teardown_appcontext
def close_connection(exception):
   db = getattr(g, '_database', None)
   if db is not None:
       db.close()




def query_db(query, args=(), one=False):
   cur = get_db().execute(query, args)
   rv = cur.fetchall()
   cur.close()
   return (rv[0] if rv else None) if one else rv





# route for the home page
@app.route('/')
def home():

   sql="""
   SELECT * FROM Game
   JOIN Studio ON Game.StudioID = Studio.StudioID;"""


   results = query_db(sql)
   return render_template('home.html', results=results)


# gammepage route
@app.route("/Game/<int:gameid>")
def game(gameid):
    spl = """SELECT * FROM Game JOIN Studio ON Game.StudioID = Studio.StudioID
    WHERE Game.Gameid = ?;"""
    result = query_db(spl, (gameid,),True)
    return render_template('game.html', game=result)

# route for the game page
@app.route('/games')
def gamepage():
  
    sql = """SELECT * FROM Game
             JOIN Studio ON Game.StudioID = Studio.StudioID;"""
    results = query_db(sql)
    return render_template('gamepage.html', results=results)

# route for the cartegory 
@app.route('/cartegory/<int:id>')
def cartegory(id):
     
    sql = """SELECT * FROM Game
             JOIN Studio ON Game.StudioID = Studio.StudioID
             WHERE Game.ClassificationID = ?"""
    results = query_db(sql,(id,))
    print(results)
    return render_template('gamepage.html', results=results)

# route for the news page
@app.route('/gamenews')
def gamenews():
  
    sql = """SELECT * FROM GameNews"""
    results = query_db(sql)
    return render_template('gamenews.html', results=results)

# route for the each news own page
@app.route('/Newspage/<int:id>')
def Newspage(id):
  
    sql = """SELECT * FROM GameNews
     WHERE GameNews.articleID = ?"""
    results = query_db(sql, (id,))
    print(results)
    
    if results:
        return render_template('Newspage.html', GameNews=results[0])
    else:
        return "no news found", 404



if __name__ == '__main__':   
   app.run(debug=True)