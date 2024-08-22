from particles import *
from grid import *
from math import *
from vpython import *
from random import *

dt = 1/15
animation_framerate = 15
number_of_particles = 1

grid_size = vec(10,10,10)
grid = Grid(grid_size=grid_size)


max_velocity = 0.5

particles = []
for i in range(0, number_of_particles):
    position = vec(randrange(1,round(grid_size.x-1)),randrange(1,round(grid_size.y-1)),randrange(1,round(grid_size.z-1)))
    velocity = vec(uniform(-max_velocity,max_velocity),uniform(-max_velocity,max_velocity),uniform(-max_velocity,max_velocity))
    particles.append(DynamicParticle(position=position, velocity=velocity, label=True))


while True:
    rate(animation_framerate)
    for p in particles:
        p.update_particle(dt, grid)

