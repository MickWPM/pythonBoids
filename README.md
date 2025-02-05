# Boids in Python

An example project, creating [Boids](https://en.wikipedia.org/wiki/Boids) in Python using [The Python Arcade Library](https://api.arcade.academy/en/latest/index.html) entities.

Boids are a way to represent a complex system using a set of simple rules. This project uses the following basic rules.

**Alignment**: steer towards the average heading of local flockmates

**Seperation**:  steer to avoid crowding local flockmates

**Cohesion**: steer to move towards the average position (center of mass) of local flockmates

![boids.png](boids.png)

Boids chase the mouse when active, status is reported in the top right.
Mouse:
- False: Mouse not active
- True: Boids will chase the mouse
Follow:
- True: Boids will follow the mouse
- False: Boids will run away from the mouse

![boids.png](boids.gif)

### Setup

1. Install the required packages

`pip3 install -r requirements.txt`

2. Run main

`python3 main.py`