from re import S
from .map import Map, Point


class Game:
    def __init__(self, player1, player2, map_width=8, map_height=14):
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.map = Map(map_width, map_height, (player1, player2))
        self.ball_position = (map_width / 2, map_height / 2)
        
        self.winning_points = ((map_width/2, -1), (map_width/2, map_height+1))
        self.n_movements = 0
    
    def reset(self):
       self.n_movements = 0
       self.current_player = self.player1
       self.ball_position = (self.map.width/2, self.map.height/2)
       self.map = Map(self.map.width, self.map.height, (self.player1, self.player2))
       self.map.points = [Point(self.map.width/2, self.map.height/2, self.player1)] 
       self.winning_points = ((self.map.width/2, -1), (self.map.width/2, self.map.height+1))
       self.map.draw_points()
       self.update_map()
       
    
    def make_move(self, x, y):
        if not self.is_move_possible(x, y):
            return False
        next_player = self._establish_player(x, y)
        self.map.add_point(x, y, self.current_player)
        self.ball_position = (x, y)
        self.current_player = next_player
        self.n_movements += 1
        return True
    
    def update_map(self):
        self.map.reset()
        self.color_possible_moves()
    
    def check_win(self):
        if self.find_possible_moves() == []:
            if self.current_player == self.player1:
                return self.player2, self.player1
            return self.player1, self.player2
        if self.ball_position == self.winning_points[0]:
            return self.player2, self.player1
        if self.ball_position == self.winning_points[1]:
            return self.player1, self.player2
        return None
        
    def is_move_possible(self, x, y):
        if (x, y) == self.ball_position:
            return False
        if abs(x - self.ball_position[0]) > 1 or abs(y - self.ball_position[1]) > 1:
            return False
        if (x, y) in self.winning_points:
            return True
        if x < 0 or x > self.map.width:
            return False
        if y < 0 or y > self.map.height:
            return False
        points = [(point.x, point.y) for point in self.map.points]
        if (((x, y), self.ball_position) in list(zip(points[1:], points[:-1])) or
            (self.ball_position, (x, y)) in list(zip(points[1:], points[:-1]))):
            return False
        if self.ball_position[0] == x and (x == 0 or x == self.map.width):
            return False
        if self.ball_position[1] == y and (y == 0 or y == self.map.height) \
            and x != self.map.width/2 and self.ball_position[0] != self.map.width/2:
            return False
        return True

    def find_possible_moves(self):
        moves = []
        for x in range(-1, self.map.width+2):
            for y in range(-1, self.map.height+2):
                if self.is_move_possible(x, y):
                    moves.append((x, y))
        return moves

    def color_possible_moves(self):
        moves = self.find_possible_moves()
        for move in moves:
            self.map.draw_point(move[0], move[1], "green")

    def _establish_player(self, x, y):
        points = [(point.x, point.y) for point in self.map.points]
        if (x, y) in points or x == 0 or x == self.map.width \
            or (y == 0 and x != self.map.width/2) or (y == self.map.height and x != self.map.width/2):
            return self.current_player
        if self.current_player == self.player1:
            return self.player2
        else:
            return self.player1
        
    def update(self, settings):
        self.player1 = settings.player_1.value
        self.player2 = settings.player_2.value
        self.map.width = int(settings.map_width)
        self.map.height = int(settings.map_height)
