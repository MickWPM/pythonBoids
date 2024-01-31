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
BOUNDRY: int = int(os.getenv('BOUNDRY'))
MAXBOIDS: int = int(os.getenv('MAXBOIDS'))


class Flock(Window):
    boids_list: list = []
    boids_x: list = []
    boids_y: list = []
    boids_vel_x: list = []
    boids_vel_y: list = []
    avg_x: float = 0
    avg_y = float = 0

    def __init__(self):
        # Call the parent __init__
        super().__init__(WIDTH, HEIGHT, WINDOW_TITLE)

        self.boids_x = list(repeat(0, MAXBOIDS))
        self.boids_y = list(repeat(0, MAXBOIDS))
        self.boids_vel_x = list(repeat(0, MAXBOIDS))
        self.boids_vel_y = list(repeat(0, MAXBOIDS))

        # Loop and create the boids
        for i in range(MAXBOIDS):
            vel_x = randrange(1,3,1)
            vel_y = randrange(1, 3, 1)

            new_boid = Boid(i, HEIGHT, WIDTH, vel_x, vel_y)
            # new_boid.debug_vals()
            self.boids_list.append(new_boid)

    def on_update(self, delta_time: float):
        for key, boid in enumerate(self.boids_list):
            self.boids_x[key] = boid.x
            self.boids_y[key] = boid.y
            # self.boids_vel_x[key] = boid.vel_x
            # self.boids_vel_y[key] = boid.vel_y
            print(self.boids_x)
            self.avg_x = fmean(self.boids_x)
            self.avg_y = fmean(self.boids_y)
            boid.vector_shift(self.avg_x, self.avg_y)
            boid.move()
            # boid.debug_vals()

    def on_draw(self):
        self.clear()
        arcade.draw_circle_filled(self.avg_x, self.avg_y,10, arcade.color.RED)
        for boid in self.boids_list:
            boid.draw()
            # boid.debug_vals()
