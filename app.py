from flask import Flask, g
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






@app.route('/')
def home():
   #home page- just the Cost, Country, and GameName.
  


   sql="""
   SELECT Game.GameName, Game.Country, Game.Cost FROM Game
   JOIN Studio ON Game.StudioID = Studio.StudioID;"""


   results = query_db(sql)
   return str(results)



@app.route("/Game/<int:gameid>")
def game(gameid):
    spl = """SELECT * FROM Game JOIN Studio ON Game.StudioID = Studio.StudioID
    WHERE Game.Gameid = ?;"""
    result = query_db(spl, (gameid,),True)
    return str(result)


 





if __name__ == '__main__':   
   app.run(debug=True)