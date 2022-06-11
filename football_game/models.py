from football_game import db

class GameInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=db.func.now())
    winner = db.Column(db.String, nullable=False)
    looser = db.Column(db.String, nullable=False)
    n_movements = db.Column(db.Integer, nullable=False)
    vs_computer = db.Column(db.Boolean, nullable=False)

class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    player_1 = db.Column(db.String, nullable=False)
    player_2 = db.Column(db.String, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
