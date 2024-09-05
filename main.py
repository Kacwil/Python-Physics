from particles import *
from grid import *
from math import *
from vpython import *
from random import *

dt = 1/1000
animation_framerate = 10000
number_of_particles = 0

grid_size = vec(10,10,10)
grid = Grid(grid_size=grid_size)


max_velocity = 0.25

particles = []
for i in range(0, number_of_particles):
    position = vec(randrange(1,round(grid_size.x-1)),randrange(1,round(grid_size.y-1)),randrange(1,round(grid_size.z-1)))
    velocity = vec(uniform(-max_velocity,max_velocity),uniform(-max_velocity,max_velocity),uniform(-max_velocity,max_velocity))
    particles.append(DynamicParticle(position=position, velocity=velocity, label=True, id=i))

i = 0
while True:
    i += 1
    rate(animation_framerate)
    for p in particles:
        #util.draw_label(p, -p.id)
        p.update_particle(dt, grid)

    if i % 5000 == 0:
        position = vec(randrange(1,round(grid_size.x-1)),randrange(1,round(grid_size.y-1)),randrange(1,round(grid_size.z-1)))
        velocity = vec(uniform(-max_velocity,max_velocity),uniform(-max_velocity,max_velocity),uniform(-max_velocity,max_velocity))
        particles.append(DynamicParticle(position=position, velocity=velocity, label=True, id=i))

    print(i)