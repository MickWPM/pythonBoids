from turtle import Turtle

class Flock(Turtle):
    count: int = 0
    boids: list[Turtle] = []

    def create_boids(self, count: int) -> None:
        pass
        # work to go to make this a flock