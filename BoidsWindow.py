import os
import arcade
from dotenv import load_dotenv

import BoidVisualiser
from Flock import Flock
from Mouse import Mouse

load_dotenv()

WIDTH: int = int(os.getenv('WIDTH'))
HEIGHT: int = int(os.getenv('HEIGHT'))
MAXBOIDS: int = int(os.getenv('MAXBOIDS'))
RANGE_MIN: int = int(os.getenv('RANGE_MIN'))
RANGE_FOV: int = int(os.getenv('RANGE_FOV'))

BUTTON_LEFT: int = 1
BUTTON_RIGHT: int = 4


class BoidsWindow(arcade.Window):
    buffer: int = 15

    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "The Boid Simulator")

        self.mouse = Mouse()

        self.flocks = [Flock(WIDTH, HEIGHT, MAXBOIDS, RANGE_MIN, RANGE_FOV),
                       Flock(WIDTH, HEIGHT, MAXBOIDS, RANGE_MIN, RANGE_FOV),
                       Flock(WIDTH, HEIGHT, MAXBOIDS, RANGE_MIN, RANGE_FOV),
                       ]
        
        BoidVisualiser.setup_batches()
        arcade.enable_timings()
            

    def on_update(self, delta_time: float):
        for flock in self.flocks:
            flock.update(self.mouse)

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

        # Add Text
        arcade.draw_text(f"Mouse: {self.mouse.active}",
                         WIDTH - 150,
                         HEIGHT - 50,
                         [255, 255, 255, 128],
                         12)
        arcade.draw_text(f"Follow: {self.mouse.chase}",
                         WIDTH - 150,
                         HEIGHT - 70,
                         [255, 255, 255, 128],
                         12)

        # Draw mouse
        if self.mouse.active:
            arcade.draw_circle_filled(self.mouse.x,
                                      self.mouse.y,
                                      5,
                                      arcade.color.GREEN)

        # Draw each flock
        for flock in self.flocks:
            flock.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """
        if self.mouse.active:
            self.mouse.x = x
            self.mouse.y = y
        else:
            self.mouse.x = 0
            self.mouse.y = 0

    def on_mouse_press(self, x, y, button, modifiers):
        if button == BUTTON_LEFT:
            self.mouse.active = not self.mouse.active

        if button == BUTTON_RIGHT:
            self.mouse.chase = not self.mouse.chase
