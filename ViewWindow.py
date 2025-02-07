from dataclasses import dataclass


@dataclass
class ViewWindow:
    """
    A dataclass representing the state of the mouse in the boid simulation.

    Attributes:
        active (bool): Indicates if the mouse interaction is active.
        chase (bool): Determines if boids should chase (True) or flee (False) the mouse.
        x (int): The x-coordinate of the mouse cursor.
        y (int): The y-coordinate of the mouse cursor.
    """
    width: int = 0
    height: int = 0
    buffer: int = 0
