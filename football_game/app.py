import base64
from email.mime import image
from multiprocessing.dummy import current_process
import os

from flask import jsonify, redirect, request, render_template

from football_game import app, db
from football_game.game import Game
from football_game.models import GameInfo, Setting
from football_game.settings import Settings, Color
from football_game.ai import computer_move

game = Game(Settings.player_1.value, Settings.player_2.value,
            Settings.map_width, Settings.map_height)
game.reset()
game.map.save_image(os.path.join(Settings.STATIC_DIR, Settings.IMAGE_DIR))

def handle_click(x, y):
    y = y - game.map.BLOCKSIZE
    r = game.map.POINT_SIZE/game.map.BLOCKSIZE
    x_rounded, y_rounded = round(x/game.map.BLOCKSIZE), round(y/game.map.BLOCKSIZE)
    x, y = x/game.map.BLOCKSIZE, y/game.map.BLOCKSIZE
    if abs(x-x_rounded) < r and abs(y-y_rounded) < r:
        return x_rounded, y_rounded
    return None


@app.route("/win/<player>")
def win(player):
    return render_template("win.html", player=player.upper(), color=player)


@app.route("/gamevsplayer/", methods=["GET", "POST"])
def game_vs_player():
    if request.method == 'GET':
            im_b64 = game.map.get_image_base64()
            return render_template('game.html', image=im_b64)
    if request.method == 'POST':
        data = request.get_json()
        x, y = data["x"], data["y"]
        if handle_click(x, y):
            x, y = handle_click(x, y)           
        if game.make_move(x, y):
            if game.check_win():
                players = game.check_win()
                new_game = GameInfo(winner=players[0].capitalize(), looser=players[1].capitalize(),
                                    vs_computer=False, n_movements=game.n_movements)
                db.session.add(new_game)
                db.session.commit()
                game.reset()
                return jsonify({"location": "/win/{}".format(players[0]), "win": True})
        game.update_map()
        im_b64 = game.map.get_image_base64()
        return jsonify({"location": "/gamevsplayer", "win": False, "image": im_b64})


@app.route("/gamevspc/", methods=["GET", "POST"])
def game_vs_pc():
    if request.method == 'GET':
            im_b64 = game.map.get_image_base64()
            return render_template('game.html', image=im_b64)
    if request.method == 'POST':
        data = request.get_json()
        x, y = data["x"], data["y"]
        if handle_click(x, y):
            x, y = handle_click(x, y)           
        if game.make_move(x, y):
            if game.check_win():
                players = game.check_win()
                new_game = GameInfo(winner=players[0].capitalize(), looser=players[1].capitalize(),
                                    vs_computer=False, n_movements=game.n_movements)
                db.session.add(new_game)
                db.session.commit()
                game.reset()
                return jsonify({"location": "/win/{}".format(players[0]), "win": True})

            print('sasasa')
            while game.current_player == game.player2:
                print('bro')
                game.make_move(*computer_move(game))
                game.update_map()
                if game.check_win():
                    players = game.check_win()
                    new_game = GameInfo(winner=players[0].capitalize(), looser=players[1].capitalize(),
                                        vs_computer=False, n_movements=game.n_movements)
                    db.session.add(new_game)
                    db.session.commit()
                    game.reset()
                    return jsonify({"location": "/win/{}".format(players[0]), "win": True})
                
        game.update_map()
        im_b64 = game.map.get_image_base64()
        return jsonify({"location": "/gamevspc", "win": False, "image": im_b64})


@app.route('/', methods=['GET', 'POST'])
def index():
    Settings.load_from_db(Setting)
    game.update(Settings)
    game.reset()
    game.map.save_image(os.path.join(Settings.STATIC_DIR, Settings.IMAGE_DIR))
    return render_template('index.html')


@app.route('/history/')
def history():
    games = GameInfo.query.all() 
    return render_template('history.html', games=games)


@app.route('/settings/', methods=['GET', 'POST'])
def settings():
    if request.method == 'GET':
        return render_template('settings.html', settings=Settings, colors=[e. value for e in Color])
    if request.method == 'POST':
        data = request.form
        Settings.update_from_form(data)
        Settings.post_to_db(Setting, db)
        game.update(Settings)
        game.map.save_image(os.path.join(Settings.STATIC_DIR, Settings.IMAGE_DIR))
        return redirect('/')
