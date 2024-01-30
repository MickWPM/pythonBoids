#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python Implementation of the Boid Algorithm
"""
from turtle import Screen
from boid import Boid

__version__ = '0.1'

WIDTH: int = 900
HEIGHT: int = 600
BOUNDRY: int = 1
MAXBOIDS: int = 20

window = Screen()
window.setup(WIDTH, HEIGHT)
window.title("Python Boid Algorithm Demo")
window.tracer(0)

flock: list = []

for i in range(MAXBOIDS):
    flock.append(Boid())
    flock[i].init_boid(i, HEIGHT, WIDTH)
    flock[i].init_velocity(0.1, 0.2)

while True:
    for i in range(MAXBOIDS):
        flock[i].update_pos()
        flock[i].boundry_check()

    window.update()
