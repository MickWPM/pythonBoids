import arcade
from random import randrange
from math import atan, sin, cos, sqrt, pi


class Boid():
    id: int = 0
    x: float = 0
    y: float = 0
    width: int = 0
    height: int = 0
    vel_x: float = 0
    vel_y: float = 0
    vel_xy: float = 0
    theta: float = 0
    window_height: int = 0
    window_width: int = 0
    colour: list = []

    def __init__(self, id: int, height: int, width: int, x_vel: int, y_vel: int):
        self.id = id
        self.window_height = height
        self.window_width = width
        self.x = randrange(round(width / 4), round(width - (width / 4)), 1)
        self.y = randrange(round(height / 4), round(height - (height / 4)), 1)
        self.vel_x = x_vel
        self.vel_y = y_vel
        self.theta = atan(y_vel/x_vel)
        self.vel_xy = sqrt(self.vel_x**2 + self.vel_y**2)
        self.width = 10
        self.height = 30
        self.colour = [255, 255, 255, 255]

    def draw(self) -> None:
        # Create x,y points for triangle, based on current self x,y
        x1 = self.x - self.width
        y1 = self.y
        x2 = self.x + self.width
        y2 = self.y
        # x3 = self.x
        # y3 = self.y + self.height

        # Transpose - using trig, a is y, b is x
        #  todo: fix this, it doesn't work and creates a flat triangle
        if self.vel_x == 0:
            self.theta = atan(self.vel_y)
        else:
            self.theta = atan(self.vel_y / self.vel_x)
        # a = round(self.width * sin(self.theta))
        # b = round(self.width * cos(self.theta))
        # # print(f"1 a:{a} b:{b}")
        # x1 = self.x - b
        # y1 = self.y - a
        # x2 = self.x + b
        # y2 = self.y + a
        # Calculate the heading and adjust for x3
        a = abs(round((self.height) * sin(self.theta)))
        b = abs(round((self.height) * cos(self.theta)))
        # print(f"2 a:{a} b:{b}")
        if self.vel_x < 0:
            x3 = self.x - b
        else:
            x3 = self.x + b
        if self.vel_y < 0:
            y3 = self.y - a
        else:
            y3 = self.y + a
        # todo: Debug print lines - remove once above is resolved
        # print(f"x:{self.x} x1:{self.x - x1} x2:{self.x - x2} x3:{self.x - x3}")
        # print(f"y:{self.y} y1:{self.y - y1} y2:{self.y - y2} y3:{self.y - y3}")
        # print(f"id:{self.id} vel_x:{self.vel_x}, vel_y:{self.vel_y}")
        # print(f"id:{self.id} theta:{degrees(self.theta)} x1:{x1} y1:{y1} x2:{x2} y2:{y2} x3:{x3} y3:{y3}")

        # heading vector
        arcade.draw_line(self.x, self.y, x3, y3, arcade.color.GRAY, 2)
        # Boid - triangle
        arcade.draw_triangle_filled(x1, y1, x2, y2, x3, y3, (255,255,255, 255))

    def move(self) -> None:
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

    def vector_shift(self, avg_x: float, avg_y: float) -> None:
        # Testing out Cohesion
        self.vel_x += (self.x + avg_x) * 0.001
        self.vel_y += (self.y + avg_y) * 0.001

    def debug_vals(self) -> None:
        print(f"Ball [{self.id}]x: {self.x} y: {self.y} x_vel:{self.vel_x} y_vel:{self.vel_y}")