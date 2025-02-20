import arcade
#from math import atan, sin, cos, sqrt
from math import sqrt

from Mouse import Mouse
from ViewWindow import ViewWindow


class Boid():
    def __init__(self,
                 flock_count: int,
                 pos_x: float,
                 pos_y: float,
                 x_vel: int,
                 y_vel: int,
                 colour: list,
                 boid_width: int,
                 boid_height: int,
                 range_min: int,
                 range_fov: int,
                 speed_max: int,
                 view_window: ViewWindow) -> None:
        """
         Boid constructor
         :param flock_count: number of boids in flock
         :param pos_x: x position of boid
         :param pos_y: y position of boid
         :param x_vel: x velocity of boid
         :param y_vel: y velocity of boid
         :param colour: colour of boid
         :param boid_width: width of boid
         :param boid_height: height of boid
         :param range_min: minimum range of boid
         :param range_fov: minimum range of boid
         :param speed_max: maximum speed of boid
         :param view_window: view window dataclass
        """
        self.debug: bool = False
        # Set initial boid properties
        self.x: float = pos_x
        self.y: float = pos_y
        self.vel_x: float = x_vel
        self.vel_y: float = y_vel
        self.colour: list = colour
        self.theta: float = 0
        self.width: int = boid_width
        self.height: int = boid_height
        self.range_min: int = range_min
        self.range_fov: int = range_fov
        self.speed_min: int = 1
        self.speed_max: int = speed_max
        self.flock_count: int = flock_count

        # Define window parameters
        self.window_height: int = view_window.height
        self.window_width: int = view_window.width
        self.buffer: int = view_window.buffer
        self.buffer_turn: int = int(view_window.buffer / 2)
        self.mouse: Mouse = Mouse()

    # def move(self, boids_x: list, boids_y: list, boids_vel_x: list, boids_vel_y: list) -> None:
    def move(self, boid_flock: list, mouse: Mouse, predators = None) -> None:
        """
        Move the boid
        """
        self.mouse = mouse
        seperation_dx: float = 0
        separation_dy: float = 0
        alignment_xvel: float = 0
        alignment_yvel: float = 0
        cohesion_xavg: float = 0
        cohesion_yavg: float = 0
        neighbour_count: int = 0
        mouse_velx: float = 0
        mouse_vely: float = 0

        mouse_factor = 0.005

        if predators is not None:
            max_distance = 99999
            for predator_list in predators:
                for predator in predator_list.get_boid_list():
                    dx = predator.x - self.x
                    dy = predator.y - self.y
                    distance = sqrt(dx ** 2 + dy ** 2)
                    max_distance = min(max_distance, distance)
            
            if max_distance < self.range_fov:
                mouse_velx = (-dx / distance) * mouse_factor * 500
                mouse_vely = (-dy / distance) * mouse_factor * 500

        mouse_distance = 9999
        if self.mouse.active:
            dx = self.mouse.x - self.x
            dy = self.mouse.y - self.y
            distance = sqrt(dx ** 2 + dy ** 2)
            mouse_distance = distance

            if self.mouse.chase:
                mouse_velx = dx * mouse_factor
                mouse_vely = dy * mouse_factor
            else:
                if distance < self.range_fov:
                    mouse_velx = (-dx / distance) * mouse_factor * 10
                    mouse_vely = (-dy / distance) * mouse_factor * 10

        alignment_distance = min(self.range_fov, mouse_distance)
        # Get the flock position and velocity data
        for boid in boid_flock:
            boid_range = sqrt((self.x - abs(boid.x)) ** 2 + (self.y - abs(boid.y)) ** 2)
            # Separation when too close
            if boid_range <= self.range_min:
                seperation_dx += self.x - boid.x
                separation_dy += self.y - boid.y
            # Alignment and Cohesion when in range
            if boid_range <= alignment_distance:
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
        self.vel_x += seperation_x + alignment_x + cohesion_x + mouse_velx
        self.vel_y += seperation_y + alignment_y + cohesion_y + mouse_vely

        # Set speed limits
        self.speed_limit()

        # Avoid the wall
        self.avoid_wall()

        # Update position with new velocity
        self.update_position()

    def speed_limit(self):
        speed = sqrt(self.vel_x * self.vel_x + self.vel_y * self.vel_y)
        if speed == 0:
            self.vel_x = self.speed_min
            self.vel_y = self.speed_min
        elif speed > self.speed_max:
            self.vel_x = (self.vel_x / speed) * self.speed_max
            self.vel_y = (self.vel_y / speed) * self.speed_max
        elif speed < self.speed_min:
            self.vel_x = (self.vel_x / speed) * self.speed_min
            self.vel_y = (self.vel_y / speed) * self.speed_min

    def avoid_wall(self):
        if self.x < (0 + self.buffer):
            self.vel_x = self.vel_x + self.buffer_turn
        if self.x > (self.window_width - self.buffer):
            self.vel_x = self.vel_x - self.buffer_turn
        if self.y < (0 + self.buffer):
            self.vel_y = self.vel_y + self.buffer_turn
        if self.y > (self.window_height - self.buffer):
            self.vel_y = self.vel_y - self.buffer_turn

    def update_position(self):
        self.x += self.vel_x
        self.y += self.vel_y

    def debug_vals(self) -> None:
        print(f"Boid x: {self.x} y: {self.y} x_vel:{self.vel_x} y_vel:{self.vel_y}")
"""
    def generate_theta(self) -> None:
        if self.vel_x == 0:
            self.theta = atan(self.vel_y)
        else:
            self.theta = atan(self.vel_y / self.vel_x)
            """
