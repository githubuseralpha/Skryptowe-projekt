import base64
from io import BytesIO
from PIL import Image, ImageDraw


class Point:
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.player = player


class Map:
    BLOCKSIZE = 43
    POINT_SIZE = 6
    
    def __init__(self, width, height, colors):
        assert width % 2 == 0 and height % 2 == 0, "Map size must be even"
        self.width = width
        self.height = height
        self.points = []
        self.colors = colors
        self.image = Image.new("RGB", (width*Map.BLOCKSIZE, (height+2)*Map.BLOCKSIZE), "#3f6c43")
        self.draw = ImageDraw.Draw(self.image)
        self.render_map()

    def reset(self):
        self.image = Image.new("RGB", (self.width*Map.BLOCKSIZE, (self.height+2)*Map.BLOCKSIZE), "#3f6c43")
        self.draw = ImageDraw.Draw(self.image)
        self.render_map()
        self.draw_points()

    def add_point(self, x, y, player):
        self.points.append(Point(x, y, player))
        
    def render_gate(self, player, is_first):
        if is_first:
            y1 = 0
            y2 = Map.BLOCKSIZE
        else:
            y1 = (self.height+2)*Map.BLOCKSIZE
            y2 = (self.height+1)*Map.BLOCKSIZE
        self.draw.line(((self.width/2-1) * Map.BLOCKSIZE, y1,
                        (self.width/2+1) * Map.BLOCKSIZE, y1), fill=player, width=5) 
        self.draw.line(((self.width/2-1) * Map.BLOCKSIZE, y1,
                        (self.width/2-1) * Map.BLOCKSIZE, y2), fill=player, width=5)
        self.draw.line(((self.width/2+1) * Map.BLOCKSIZE, y1,
                        (self.width/2+1) * Map.BLOCKSIZE, y2), fill=player, width=5)
    
    def render_map(self):
        for i in range(self.width+1):
            for j in range(self.height+1):
                self.draw_point(i, j, "#233c25")
        self.render_gate(self.colors[0], True)
        self.render_gate(self.colors[1], False)
                        
    def draw_points(self):
        if len(self.points) == 0:
            return
        last_x, last_y = self.points[0].x, self.points[0].y
        for i, point in enumerate(self.points):
            if i != 0: 
                self.draw.line((last_x*Map.BLOCKSIZE, (last_y+1)*Map.BLOCKSIZE,
                                (point.x*Map.BLOCKSIZE, (point.y+1)*Map.BLOCKSIZE)),
                            fill=point.player, width=2)
                last_x, last_y = point.x, point.y
            self.draw_point(point.x, point.y, point.player)
            
    def draw_point(self, x, y, player):
        self.draw.ellipse((x*Map.BLOCKSIZE-Map.POINT_SIZE, (y+1)*Map.BLOCKSIZE-Map.POINT_SIZE,
                           x*Map.BLOCKSIZE+Map.POINT_SIZE, (y+1)*Map.BLOCKSIZE+Map.POINT_SIZE),
                           fill=player)
    
    def save_image(self, filename):
        self.image.save(filename)
        
    def get_image_base64(self):
        img_buffer = BytesIO()
        self.image.save(img_buffer, format='PNG')
        byte_data = img_buffer.getvalue()
        base64_str = base64.b64encode(byte_data)
        return base64_str.decode('utf-8')
