import arcade
from random import randrange


class Boid():
    id: int = 0
    x: float = 0
    y: float = 0
    width: int = 0
    height: int = 0
    vel_x: int = 0
    vel_y: int = 0
    window_height: int = 0
    window_width: int = 0
    colour: list = []

    def __init__(self, id: int, height: int, width: int, x_vel: int, y_vel: int):
        self.id = id
        self.window_height = height
        self.window_width = width
        self.x = randrange(0, width)
        self.y = randrange(0,height)
        self.vel_x = x_vel
        self.vel_y = y_vel
        self.width = 10
        self.height = 30
        self.colour = [255, 255, 255, 255]

    def draw(self):
        x1 = self.x - self.width
        y1 = self.y
        x2 = self.x + self.width
        y2 = self.y
        x3 = self.x
        y3 = self.y + self.height
        arcade.draw_triangle_filled(x1, y1, x2, y2, x3, y3, (255,255,255, 255))

    def move(self):
        # move forward
        self.x += self.vel_x
        self.y += self.vel_y

        # Wall bounding
        if self.x < 0:
            self.vel_x = -self.vel_x
        if self.x > self.window_width:
            self.vel_x = -self.vel_x
        if self.y < 0:
            self.vel_y = -self.vel_y
        if self.y > self.window_height:
            self.vel_y = -self.vel_y

    def debug_vals(self):
        print(f"Ball [{self.id}]x: {self.x} y: {self.y} x_vel:{self.vel_x} y_vel:{self.vel_y}")