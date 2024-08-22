from math import *
from random import *
from vpython import *

def grid_place_has_changed(new_position, old_position):
    if round(new_position.x) != round(old_position.x):
        return True
    
    if round(new_position.y) != round(old_position.y):
        return True
    
    if round(new_position.z) != round(old_position.z):
        return True
    
    return False

def find_position_for_static_wall_particles(x,y,z, max_size):

    positions = []

    for i in range(-2,2):
        x_offset = i * 0.13
        for j in range(-2,2):
            y_offset = j * 0.13
            for k in range(-2,2):
                z_offset = k * 0.13

                pos = vec(x + x_offset, y + y_offset, z + z_offset)

                if x == 0:
                    pos = vec(0, pos.y, pos.z)
                if y == 0:
                    pos = vec(pos.x, 0, pos.z)
                if z == 0:
                    pos = vec(pos.x, pos.y, 0)

                if x == max_size.x:
                    pos = vec(max_size.x, pos.y, pos.z)
                if y == max_size.y:
                    pos = vec(pos.x, max_size.y, pos.z)
                if z == max_size.z:
                    pos = vec(pos.x, pos.y, max_size.z)

                if pos not in positions:
                    positions.append(pos)

    return positions