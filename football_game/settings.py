from enum import Enum

class Color(Enum):
    RED = "red"
    BLUE = "blue"
    BLACK = "black"
    YELLOW = "yellow"
    PURPLE = "purple"
    ORANGE = "orange"

class Settings:
    map_width=8
    map_height=14
    player_1=Color.RED
    player_2=Color.BLUE
    difficulty=1
    
    STATIC_DIR = "C:\\Users\\Patryk\\football\\football_game\\static"
    IMAGE_DIR = "images/uhh.png"

    @classmethod
    def load_from_db(cls, model):
        last = model.query.order_by(model.id.desc()).first()

        assert last.difficulty in range(1, 4)
        assert last.width > 0 and last.width % 2 == 0
        assert last.height > 0 and last.height % 2 == 0
        
        cls.map_width = last.width
        cls.map_height = last.height
        cls.player_1 = Color(last.player_1)
        cls.player_2 = Color(last.player_2)
        cls.difficulty = last.difficulty
        
    @classmethod
    def update_from_form(cls, data):        
        cls.map_width = data["map_width"]
        cls.map_height = data["map_height"]
        cls.player_1 = Color(data["player_1"])
        cls.player_2 = Color(data["player_2"])
        #cls.difficulty = data["difficulty"]
        
    @classmethod
    def post_to_db(cls, model, db):
        setting = model(width=cls.map_width, height=cls.map_height,
                         player_1=cls.player_1.value, player_2=cls.player_2.value,
                         difficulty=cls.difficulty)
        db.session.add(setting)
        db.session.commit()
        
        