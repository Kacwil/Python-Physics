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

def draw_label(particle, y):
    if particle.has_label == False:
        l = label(pos=vec(-10,y,0), text=mag(particle.velocity))
        particle.label = l
        particle.has_label = True
    else:
        v = round(mag(particle.velocity),2)
        Ek = round(v*v*particle.mass*.5,2)
        Ep = round(particle.mass*9.81*particle.position.y,2)
        particle.label.text = "Velocity", v, "Kinetic", Ek, "Potential",Ep, "Total Energy", Ek+Ep

def physics_gravity():
    return vec(0,-9.81,0)

def physics_air_drag(velocity, mass):
    air_drag_constant = .5
    force = vec(0,0,0)
    force.x += copysign((velocity.x * velocity.x) * air_drag_constant, -velocity.x )
    force.y += copysign((velocity.y * velocity.y) * air_drag_constant, -velocity.y )
    force.z += copysign((velocity.z * velocity.z) * air_drag_constant, -velocity.z )
    return force / mass