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
RANGE_FOV: int = int(os.getenv('RANGE_FOV'))


class Flock(Window):
    boids_list: list = []
    boids_x: list = []
    boids_y: list = []
    max_speed: int = 0
    avg_x: float = 0
    avg_y: float = 0
    flock_width: int = 0
    flock_height: int = 0
    buffer: int = 15
    debug: bool = False
    colour: list = []

    def __init__(self):
        """
        Create the flock
        """
        super().__init__(WIDTH, HEIGHT, WINDOW_TITLE)

        self.debug = False

        self.boids_x = list(repeat(0, MAXBOIDS))
        self.boids_y = list(repeat(0, MAXBOIDS))

        self.flock_width = WIDTH - (self.buffer * 2)
        self.flock_height = HEIGHT - (self.buffer * 2)

        self.max_speed = randrange(2, 5, 1)

        self.colour = [randrange(0, 255, 1),
                       randrange(0, 255, 1),
                       randrange(0, 255, 1),
                       255]

        # Loop and create the boids
        for _ in range(MAXBOIDS):
            # Initial Position
            pos_x = randrange(0, self.flock_width, 10)
            pos_y = randrange(0, self.flock_height, 10)
            # Initial Velocity
            vel_x = randrange(-5, 5, 1)
            vel_y = randrange(-5, 5, 1)

            new_boid = Boid(MAXBOIDS,
                            pos_x,
                            pos_y,
                            vel_x,
                            vel_y,
                            self.colour,
                            RANGE_MIN,
                            RANGE_FOV,
                            self.max_speed,
                            self.flock_height,
                            self.flock_width,
                            self.buffer)
            # new_boid.debug_vals()
            self.boids_list.append(new_boid)

    def on_update(self, delta_time: float):
        for key, boid in enumerate(self.boids_list):
            boid.move(self.boids_list)

            self.boids_x[key] = boid.x
            self.boids_y[key] = boid.y

    def on_draw(self):
        self.clear()
        # Draw the border
        arcade.draw_rectangle_outline(WIDTH / 2,
                                      HEIGHT / 2,
                                      WIDTH - self.buffer,
                                      HEIGHT - self.buffer,
                                      (255, 255, 255, 128),
                                      2,
                                      0)

        # Draw the boid average position
        if self.debug:
            self.avg_x = fmean(self.boids_x)
            self.avg_y = fmean(self.boids_y)
            arcade.draw_circle_filled(self.avg_x, self.avg_y, 5, arcade.color.RED)

        for boid in self.boids_list:
            boid.draw()
            if self.debug:
                boid.debug_vals()
