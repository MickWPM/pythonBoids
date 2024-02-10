import arcade
from random import randrange
from math import atan, sin, cos, sqrt, radians
from statistics import fmean
from numpy import clip


class Boid():
    id: int = 0
    x: float = 0
    y: float = 0
    width: int = 0
    height: int = 0
    vel_x: float = 0
    vel_y: float = 0
    speed_max: float = 0
    speed_min: float = 0
    leader: bool = False
    theta: float = 0
    range_min: int = 0
    range_fov: int = 0
    window_height: int = 0
    window_width: int = 0           # Window width
    buffer: int = 0                 # Buffer from the edge of the window to the frame
    colour: list = []
    debug: bool = False

    def __init__(self, id: int, height: int, width: int, buffer: int, x_vel: int, y_vel: int, range_min: int, range_fov: int, leader: bool) -> None:
        self.id = id
        self.debug = False

        # Set initial position and velocity
        self.x = randrange(round(width / 4), round(width - (width / 4)), 1)
        self.y = randrange(round(height / 4), round(height - (height / 4)), 1)
        self.vel_x = x_vel
        self.vel_y = y_vel
        self.speed_max = 10
        self.speed_min = 1
        self.theta = atan(y_vel/x_vel)
        self.leader = leader
        self.range_min = range_min
        self.range_fov = range_fov

        # Define the boid
        self.width = 5
        self.height = 10
        self.colour = [255, 255, 255, 255]

        # Define window parameters
        self.window_height = height
        self.window_width = width
        self.buffer = buffer

    def draw(self) -> None:
        # Create x,y points for triangle, based on current self x,y
        x1 = self.x - self.width
        y1 = self.y
        x2 = self.x + self.width
        y2 = self.y

        # Transpose - using trig, a is y, b is x
        if self.vel_x == 0:
            self.theta = atan(self.vel_y)
        else:
            self.theta = atan(self.vel_y / self.vel_x)
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

        # heading vector
        arcade.draw_line(self.x, self.y, x3, y3, arcade.color.GRAY, 2)
        # Boid - triangle
        if self.leader:
            arcade.draw_triangle_filled(x1, y1, x2, y2, x3, y3, (128,128,0, 255))
        else:
            arcade.draw_triangle_filled(x1, y1, x2, y2, x3, y3, (255, 255, 255, 255))
        # draw range rings
        if self.debug:
            arcade.draw_circle_outline(self.x, self.y, self.range_min,(255,0,0, 200), 2,0)
            arcade.draw_circle_outline(self.x, self.y, self.range_max,(255,255,0, 150), 2,0)

    # def move(self, boids_x: list, boids_y: list, boids_vel_x: list, boids_vel_y: list) -> None:
    def move(self, boids_list: list) -> None:
        cohesion: float = 0
        # cohesion_y: float = 0
        alignment: float = 0
        # alignment_y: float = 0
        seperation: float = self.vel_x
        # seperation_y: float = self.vel_y
        xy: float = 0
        boids_x: list = []
        boids_y: list = []
        boids_vel_x: list = []
        boids_vel_y: list = []

        for boid in boids_list:
            delta_boid = sqrt((self.x - abs(boid.x))*(self.x - abs(boid.x))+(self.y - abs(boid.y))*(self.y - abs(boid.y)))
            if 0 < delta_boid < self.range_min:
                print(f"Boid close: {delta_boid}")
                if 0 < delta_boid:
                    seperation += atan(self.vel_y / self.vel_x)
                else:
                    seperation -= atan(self.vel_y / self.vel_x)

            if 0 < delta_boid < self.range_fov:
                boids_x.append(boid.x)
                boids_y.append(boid.y)
                boids_vel_x.append(boid.vel_x)
                boids_vel_y.append(boid.vel_y)

        if 0 < len(boids_x):
            # Cohesion
            cohesion = atan((self.y - fmean(boids_y)) / (self.x - fmean(boids_x)))
            # cohesion_y = atan(fmean(boids_y))
            # Alignment
            alignment = atan(fmean(boids_vel_y) / fmean(boids_vel_x))
            # alignment_y = fmean(boids_vel_y) - self.vel_y

        # Set the velocity vector for the boids
        if self.leader:
            self.theta += seperation
        else:
            self.theta += seperation + cohesion + alignment

        self.vel_x = cos(self.theta)
        self.vel_y = sin(self.theta)

        # Set speed limits
        speed = sqrt(self.vel_x * self.vel_x + self.vel_y * self.vel_y)
        if speed > self.speed_max:
            self.vel_x = (self.vel_x / speed) * self.speed_max
            self.vel_y = (self.vel_y / speed) * self.speed_max
        if 0 < speed < self.speed_min:
            self.vel_x = (self.vel_x / speed) * self.speed_min
            self.vel_y = (self.vel_y / speed) * self.speed_min


        # print(f"Velocity: {self.vel_x}::{self.vel_y}")

        # Update position with new velocity
        self.x += self.vel_x
        self.y += self.vel_y

        # Avoid the wall
        if self.x < (0 + self.buffer):
            self.vel_x = -self.vel_x
            self.x += abs(self.vel_x)
        if self.x > (self.window_width - self.buffer):
            self.vel_x = -self.vel_x
            self.x -= abs(self.vel_x)
        if self.y < (0 + self.buffer):
            self.vel_y = -self.vel_y
            self.y += abs(self.vel_y)
        if self.y > (self.window_height - self.buffer):
            self.vel_y = -self.vel_y
            self.y -= abs(self.vel_y)

    def debug_vals(self) -> None:
        print(f"Ball [{self.id}]x: {self.x} y: {self.y} x_vel:{self.vel_x} y_vel:{self.vel_y}")
