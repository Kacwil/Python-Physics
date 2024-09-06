from particles import *
from grid import *
from math import *
from vpython import *
from random import *
from cProfile import *
import pstats

dt = 1/500
animation_framerate = 100000
number_of_particles = 3

grid_size = vec(10,10,10)
grid = Grid(grid_size=grid_size)


max_velocity = 1

particles = []
for i in range(0, number_of_particles):
    position = vec(randrange(1,round(grid_size.x-1)),randrange(1,round(grid_size.y-1)),randrange(1,round(grid_size.z-1)))
    velocity = vec(uniform(-max_velocity,max_velocity),uniform(-max_velocity,max_velocity),uniform(-max_velocity,max_velocity))
    particles.append(DynamicParticle(position=position, velocity=velocity, label=True, id=i))

s1= Spring(particles[0],particles[1],2)
s2= Spring(particles[1],particles[2],2)
s3= Spring(particles[2],particles[0],2)

springs = []
springs.append(s1)
springs.append(s2)
springs.append(s3)



i = 0

with Profile() as profile:
    while True:
        i += 1
        rate(animation_framerate)

        for j in range(round(1/dt)):
            for s in springs:
               s.update(dt) 
            for p in particles:
                #util.draw_label(p, -p.id)
                p.update_particle(dt, grid)

        if i % 10 == 0:
            break

        print(i)


    results = pstats.Stats(profile)
    results.sort_stats(pstats.SortKey.TIME)
    results.print_stats()