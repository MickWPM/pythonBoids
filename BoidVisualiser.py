
import arcade
import numpy as np
from math import atan, sin, cos, sqrt

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm

def draw_flock(flock):
    for boid in flock.boids_list:
        draw(boid)

def draw(boid) -> None:
    """
    Draw the boid
    """
    # Create x,y points for triangle, based on current boid x,y
    x1 = boid.x - boid.width
    y1 = boid.y
    x2 = boid.x + boid.width
    y2 = boid.y


    velocity_vector = np.array([boid.vel_x, boid.vel_y])
    position_vector = np.array([boid.x, boid.y])

    velocity_vector_normalised = normalize(velocity_vector)
    triangle_middle_base = position_vector - velocity_vector_normalised * 15

    arcade.draw_line(position_vector[0], position_vector[1], triangle_middle_base[0], triangle_middle_base[1], arcade.color.GRAY, 2)



    # heading vector
    #arcade.draw_line(boid.x, boid.y, x3, y3, arcade.color.GRAY, 2)
    # Boid - triangle
    #arcade.draw_triangle_filled(x1, y1, x2, y2, x3, y3, boid.colour)
    # draw range rings
    #if boid.debug:
        #arcade.draw_circle_outline(boid.x, boid.y, boid.range_min, (255, 0, 0, 200), 2, 0)
    arcade.draw_circle_outline(boid.x, boid.y, 5, (255, 200, 200, 200), 2, 0)