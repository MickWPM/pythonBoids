from turtle import Turtle
from random import randrange


class Boid(Turtle):
    id: int = 0
    vel_x: int = 0
    vel_y: int = 0
    window_height: int = 0
    window_width: int = 0

    def init_boid(self, id: int, height: int, width: int):
        self.id = id
        self.window_height = height
        self.window_width = width
        self.penup()
        self.color("black")
        self.shape("arrow")
        self.left(randrange(int(-width / 2), int(width / 2), 1))
        self.forward(randrange(int(-height / 2), int(height / 2), 1))

    def init_velocity(self, x: int, y: int):
        self.vel_x = x
        self.vel_y = y

    def update_pos(self):
        self.setx(self.xcor() + self.vel_x)
        self.sety(self.ycor() + self.vel_y)

    def boundry_check(self):
        # Wall bounding
        if self.xcor() > self.window_width / 2 or self.xcor() < -self.window_width / 2:
            self.vel_x = -self.vel_x

        if self.ycor() > self.window_height / 2 or self.ycor() < -self.window_height / 2:
            self.vel_y = -self.vel_y

    def debug_vals(self):
        print(f"Ball x: {self.xcor()} y: {self.ycor()} x_vel:{self.vel_x} y_vel:{self.vel_y}")