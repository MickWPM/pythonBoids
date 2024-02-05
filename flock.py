import os
import arcade.color
from dotenv import load_dotenv
from arcade import Window
from random import randrange
from itertools import repeat
from statistics import fmean

from boids import Boid


load_dotenv()

WINDOW_TITLE = os.getenv('WINDOW_TITLE')
WIDTH: int = int(os.getenv('WIDTH'))
HEIGHT: int = int(os.getenv('HEIGHT'))
MAXBOIDS: int = int(os.getenv('MAXBOIDS'))
RANGE_MIN: int = int(os.getenv('RANGE_MIN'))
RANGE_MAX: int = int(os.getenv('RANGE_MAX'))


class Flock(Window):
    boids_list: list = []
    boids_x: list = []
    boids_y: list = []
    boids_vel_x: list = []
    boids_vel_y: list = []
    avg_x: float = 0
    avg_y: float = 0
    window_div_width: int = 0
    window_div_height: int = 0
    buffer:int = 15
    debug: bool = False

    def __init__(self):
        # Call the parent __init__
        super().__init__(WIDTH, HEIGHT, WINDOW_TITLE)

        self.debug = False

        self.boids_x = list(repeat(0, MAXBOIDS))
        self.boids_y = list(repeat(0, MAXBOIDS))
        self.boids_vel_x = list(repeat(0, MAXBOIDS))
        self.boids_vel_y = list(repeat(0, MAXBOIDS))

        # Loop and create the boids
        for i in range(MAXBOIDS):
            vel_x = randrange(1,3,1)
            vel_y = randrange(1, 3, 1)

            new_boid = Boid(i, HEIGHT, WIDTH, self.buffer, vel_x, vel_y, RANGE_MIN, RANGE_MAX)
            # new_boid.debug_vals()
            self.boids_list.append(new_boid)

    def on_update(self, delta_time: float):
        for key, boid in enumerate(self.boids_list):
            # boid.move(self.boids_x, self.boids_y, self.boids_vel_x, self.boids_vel_y)
            boid.move(self.boids_list, self.boids_x, self.boids_y, self.boids_vel_x, self.boids_vel_y)

            self.boids_x[key] = boid.x
            self.boids_y[key] = boid.y
            self.boids_vel_x[key] = boid.vel_x
            self.boids_vel_y[key] = boid.vel_y

    def on_draw(self):
        self.clear()
        # Draw the border
        arcade.draw_rectangle_outline(WIDTH/2, HEIGHT/2, WIDTH-self.buffer, HEIGHT-self.buffer, (255,255,255,128), 2,0)

        self.avg_x = fmean(self.boids_x)
        self.avg_y = fmean(self.boids_y)

        # Draw the boid average position
        if self.debug:
            arcade.draw_circle_filled(self.avg_x, self.avg_y,10, arcade.color.RED)

        for boid in self.boids_list:
            boid.draw()
            # boid.debug_vals()
