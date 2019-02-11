class Pedestrians:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.future_x = x
        self.future_y = y
        self.neighbors = {}  # key : adjacent cell, value : proba to go to this cell
        self.aggressivity = 0.5

    def move(self):
        self.x = self.future_x
        self.y = self.future_y

    def predict_move(self, direction_x, direction_y, speed=1):
        self.future_x = self.x + direction_x * speed
        self.future_y = self.y + direction_y * speed

    def getPosition(self):
        return self.x, self.y

    def predictPosition(self):
        return self.future_x, self.future_y
