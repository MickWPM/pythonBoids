from random import randrange

from Boids import Boid
from Mouse import Mouse
from ViewWindow import ViewWindow


class Flock:
    def __init__(self, width, height, max_boids, range_min, range_fov):
        """
        Create the flock
        """
        self.boids_list: list = []
        self.max_speed: int = 0
        self.avg_x: float = 0
        self.avg_y: float = 0
        self.buffer: int = 15
        self.colour: list = []

        self.view_window: ViewWindow = ViewWindow(width - (self.buffer * 2),
                                                  height - (self.buffer * 2),
                                                  self.buffer, )

        self.max_speed = randrange(3, 8, 1)
        self.colour = [randrange(0, 255, 1),
                       randrange(0, 255, 1),
                       randrange(0, 255, 1),
                       255]
        self.boid_height: int = randrange(4, 30, 1)
        self.boid_width: int = int(self.boid_height / 2)
        self.mouse = Mouse()

        # Loop and create the boids
        for _ in range(max_boids):
            # Initial Position
            pos_x = randrange(0, self.view_window.width, 10)
            pos_y = randrange(0, self.view_window.height, 10)
            # Initial Velocity
            vel_x = randrange(-5, 5, 1)
            vel_y = randrange(-5, 5, 1)

            new_boid = Boid(max_boids,
                            pos_x,
                            pos_y,
                            vel_x,
                            vel_y,
                            self.colour,
                            self.boid_width,
                            self.boid_height,
                            range_min,
                            range_fov,
                            self.max_speed,
                            self.view_window)
            # new_boid.debug_vals()
            self.boids_list.append(new_boid)

    def update(self, mouse: Mouse):
        self.mouse = mouse
        for key, boid in enumerate(self.boids_list):
            boid.move(self.boids_list, self.mouse)

    def draw(self):
        for boid in self.boids_list:
            boid.draw()
