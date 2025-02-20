
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

def setup_batches():
    global shape_list
    shape_list = arcade.ShapeElementList()

def draw_flock(flock):
    draw_flock_instanced(flock)
    #for boid in flock.boids_list:
     #  draw(boid)
    

def draw_flock_instanced(flock):
    point_list = []
    colour_list = []
    for boid in flock.boids_list:
        x1, y1, x2, y2, x3, y3 = get_triangle_points(boid)
        point_list.append((x1, y1))
        point_list.append((x2, y2))
        point_list.append((x3, y3))
        point_list.append((x3, y3))
        for i in range(4):
            colour_list.append(boid.colour)
    shape = arcade.create_rectangles_filled_with_colors(point_list, colour_list)
    shape_list.append(shape)
    shape_list.draw()
    shape_list.remove(shape)

def get_triangle_points(boid):
    # Create x,y points for triangle, based on current boid x,y
    x1 = boid.x - boid.width
    y1 = boid.y
    x2 = boid.x + boid.width
    y2 = boid.y

    # Transpose - using trig, a is y, b is x
    if boid.vel_x == 0:
        boid.theta = atan(boid.vel_y)
    else:
        boid.theta = atan(boid.vel_y / boid.vel_x)
    # Calculate the heading and adjust for x3
    a = abs(round(boid.height * sin(boid.theta)))
    b = abs(round(boid.height * cos(boid.theta)))
    # print(f"2 a:{a} b:{b}")
    if boid.vel_x < 0:
        x3 = boid.x - b
    else:
        x3 = boid.x + b
    if boid.vel_y < 0:
        y3 = boid.y - a
    else:
        y3 = boid.y + a
    return (x1, y1, x2, y2, x3, y3)
"""
    velocity_vector = np.array([boid.vel_x, boid.vel_y])
    position_vector = np.array([boid.x, boid.y])
    velocity_vector_normalised = normalize(velocity_vector)
    triangle_middle_base = position_vector - velocity_vector_normalised * 15
"""

def draw(boid) -> None:
    """
    Draw the boid
    """
    x1, y1, x2, y2, x3, y3 = get_triangle_points(boid)
    
    # heading vector
    #arcade.draw_line(boid.x, boid.y, x3, y3, arcade.color.GRAY, 2)
    # Boid - triangle
    #arcade.draw_triangle_filled(x1, y1, x2, y2, x3, y3, boid.colour)
    # draw range rings
    #if boid.debug:
        #arcade.draw_circle_outline(boid.x, boid.y, boid.range_min, (255, 0, 0, 200), 2, 0)
    arcade.draw_circle_outline(boid.x, boid.y, 5, (255, 200, 200, 200), 2, 0)