
import arcade
from math import atan, sin, cos, sqrt

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

    # heading vector
    arcade.draw_line(boid.x, boid.y, x3, y3, arcade.color.GRAY, 2)
    # Boid - triangle
    arcade.draw_triangle_filled(x1, y1, x2, y2, x3, y3, boid.colour)
    # draw range rings
    if boid.debug:
        arcade.draw_circle_outline(boid.x, boid.y, boid.range_min, (255, 0, 0, 200), 2, 0)
