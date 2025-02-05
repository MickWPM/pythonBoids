import arcade
from random import randrange
from math import atan, sin, cos, sqrt, radians
from statistics import fmean
from numpy import clip


class Boid():
    # Position and velocity
    x: float = 0
    y: float = 0
    vel_x: float = 0
    vel_y: float = 0
    speed_max: float = 0
    speed_min: float = 1
    # Boid properties
    width = 5
    height = 10
    colour: list = []
    theta: float = 0
    # Flock fields
    flock_count: int = 0
    range_min: int = 0
    max_change: int = 0
    range_fov: int = 0
    # Window details
    window_height: int = 0
    window_width: int = 0
    buffer: int = 0  # Buffer from the edge of the window to the frame
    buffer_turn: int = 0
    debug: bool = False

    def __init__(self,
                 flock_count: int,
                 pos_x: float,
                 pos_y: float,
                 x_vel: int,
                 y_vel: int,
                 colour: list,
                 range_min: int,
                 range_fov: int,
                 speed_max: int,
                 window_height: int,
                 window_width: int,
                 buffer: int) -> None:
        """
         Boid constructor
         :param flock_count: number of boids in flock
         :param window_height: height of the window
         :param window_width: width of the window
         :param buffer: buffer size of the window
         :param x_vel: x velocity of the boid
         :param y_vel: y velocity of the boid
         :param colour: colour of the boid
         :param range_min: minimum range of the boid
         :param range_fov: fov of the boid
        """
        self.flock_count = flock_count
        self.debug = False

        # Set initial position and velocity
        self.x = pos_x
        self.y = pos_y
        self.vel_x = x_vel
        self.vel_y = y_vel
        self.colour = colour
        # self.generate_theta()
        self.range_min = range_min
        self.range_fov = range_fov
        self.speed_max = speed_max

        # Define window parameters
        self.window_height = window_height
        self.window_width = window_width
        self.buffer = buffer
        self.buffer_turn = int(buffer / 2)

    def draw(self) -> None:
        """
        Draw the boid
        """
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
        a = abs(round(self.height * sin(self.theta)))
        b = abs(round(self.height * cos(self.theta)))
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
        arcade.draw_triangle_filled(x1, y1, x2, y2, x3, y3, self.colour)
        # draw range rings
        if self.debug:
            arcade.draw_circle_outline(self.x, self.y, self.range_min, (255, 0, 0, 200), 2, 0)

    # def move(self, boids_x: list, boids_y: list, boids_vel_x: list, boids_vel_y: list) -> None:
    def move(self, boid_flock: list) -> None:
        """
        Move the boid
        """
        seperation_dx: float = 0
        separation_dy: float = 0
        alignment_xvel: float = 0
        alignment_yvel: float = 0
        cohesion_xavg: float = 0
        cohesion_yavg: float = 0
        neighbour_count: int = 0

        # Get the flock position and velocity data
        for boid in boid_flock:
            boid_range = sqrt((self.x - abs(boid.x)) ** 2 + (self.y - abs(boid.y)) ** 2)
            # Separation when too close
            if boid_range <= self.range_min:
                seperation_dx += self.x - boid.x
                separation_dy += self.y - boid.y
            # Alignment and Cohesion when in range
            if boid_range <= self.range_fov:
                alignment_xvel += boid.vel_x
                alignment_yvel += boid.vel_y
                cohesion_xavg += boid.x
                cohesion_yavg += boid.y
                neighbour_count += 1

        seperation_factor = 0.1
        alignment_factor = 0.05
        cohesion_factor = 0.01

        seperation_x = seperation_dx * seperation_factor
        seperation_y = separation_dy * seperation_factor
        alignment_x = ((alignment_xvel / neighbour_count) - self.vel_x) * alignment_factor
        alignment_y = ((alignment_yvel / neighbour_count) - self.vel_y) * alignment_factor
        cohesion_x = ((cohesion_xavg / neighbour_count) - self.x) * cohesion_factor
        cohesion_y = ((cohesion_yavg / neighbour_count) - self.y) * cohesion_factor

        # Update velocity with boid properties
        self.vel_x += seperation_x + alignment_x + cohesion_x
        self.vel_y += seperation_y + alignment_y + cohesion_y

        # Set speed limits
        speed = sqrt(self.vel_x * self.vel_x + self.vel_y * self.vel_y)
        if speed > self.speed_max:
            self.vel_x = (self.vel_x / speed) * self.speed_max
            self.vel_y = (self.vel_y / speed) * self.speed_max
        if speed < self.speed_min:
            self.vel_x = (self.vel_x / speed) * self.speed_min
            self.vel_y = (self.vel_y / speed) * self.speed_min

        # Avoid the wall
        if self.x < (0 + self.buffer):
            self.vel_x = self.vel_x + self.buffer_turn
        if self.x > (self.window_width - self.buffer):
            self.vel_x = self.vel_x - self.buffer_turn
        if self.y < (0 + self.buffer):
            self.vel_y = self.vel_y + self.buffer_turn
        if self.y > (self.window_height - self.buffer):
            self.vel_y = self.vel_y - self.buffer_turn

        # Update position with new velocity
        self.x += self.vel_x
        self.y += self.vel_y

    def debug_vals(self) -> None:
        print(f"Boid x: {self.x} y: {self.y} x_vel:{self.vel_x} y_vel:{self.vel_y}")

    def generate_theta(self) -> None:
        if self.vel_x == 0:
            self.theta = atan(self.vel_y)
        else:
            self.theta = atan(self.vel_y / self.vel_x)
