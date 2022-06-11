from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site2.db'
db = SQLAlchemy(app)

@app.cli.command("init_db")
def init_db():
    db.drop_all()
    db.create_all()
    gi = GameInfo(winner="Red", looser="Blue", n_movements=0, vs_computer=False)
    s = Setting(width=8, height=14, player_1="red", player_2="blue", difficulty=1)
    db.session.add(gi)
    db.session.add(s)
    db.session.commit()

from football_game.app import *

    