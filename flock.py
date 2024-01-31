import os
from dotenv import load_dotenv
from arcade import Window
from boids import Boid

load_dotenv()

WINDOW_TITLE = os.getenv('WINDOW_TITLE')
WIDTH: int = int(os.getenv('WIDTH'))
HEIGHT: int = int(os.getenv('HEIGHT'))
BOUNDRY: int = int(os.getenv('BOUNDRY'))
MAXBOIDS: int = int(os.getenv('MAXBOIDS'))


class Flock(Window):
    boids_list: list = []

    def __init__(self):
        # Call the parent __init__
        super().__init__(WIDTH, HEIGHT, WINDOW_TITLE)

        # Loop and create the boids
        for i in range(MAXBOIDS):
            new_boid = Boid(i, HEIGHT, WIDTH, 3, 3)
            # new_boid.debug_vals()
            self.boids_list.append(new_boid)

    def on_update(self, delta_time: float):
        for boid in self.boids_list:
            boid.move()
            # boid.debug_vals()

    def on_draw(self):
        self.clear()
        for boid in self.boids_list:
            boid.draw()
            # boid.debug_vals()
