#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python Implementation of the Boid Algorithm
"""
import arcade

from BoidsWindow import BoidsWindow

__version__ = '0.1'


def main():
    BoidsWindow()
    arcade.run()


if __name__ == "__main__":
    main()