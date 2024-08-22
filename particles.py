from vpython import *
import util

class StaticParticle:
    def __init__(self, position=vec(2,2,2), radius=0.5, visible=False, COR=1):
        self.position = position
        self.radius = radius
        self.is_static = True
        self.COR = COR #Coefficient of restituion
        if visible:
            self.drawSphere()

    def drawSphere(self):
        self.sphere = sphere(pos=self.position, radius=self.radius, color=vec(1,0,0), opacity=0.3)


class DynamicParticle(StaticParticle):
    def __init__(self, position=vec(2,2,2), velocity=vec(0,0,0), acceleration=vec(0,0,0), mass=1 ,radius=0.1, visible=True, COR=0.75, label=False):
        super().__init__(position, radius, visible, COR)

        self.is_static = False
        self.last_position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.mass = mass
        self.has_label = label

        if label:
            self.drawLabel()

    def drawSphere(self):
        self.sphere = sphere(pos=self.position, radius=self.radius, color=vec(random(),random(),random()))
    
    def drawLabel(self):
        self.label = label(pos=vec(-1,-1,-1), text=round(mag(self.velocity),2))
    
    def update_particle(self, dt, grid):

        for i in range(0, round(1/dt)):
            self.physics_update(dt)
            self.grid_update(grid)

            for neighbour in grid.get_particles_in_neighbourhood(self):
                if self.check_for_collision(neighbour):
                    self.collision(neighbour, dt)


        if self.has_label:
            self.label.text = round(mag(self.velocity),2)

    def physics_update(self, dt):
        self.last_position = self.position
        self.velocity = self.velocity + dt * self.acceleration
        self.acceleration = vec(0,0,0)
        self.position = self.position + dt * self.velocity
        self.sphere.pos = self.position
        print(self.velocity)

    def grid_update(self, grid):
        if util.grid_place_has_changed(self.position, self.last_position):
            grid.update_grid(self)

    def check_for_collision(self, other):
        distance = dist((self.position.x,self.position.y,self.position.z), (other.position.x,other.position.y,other.position.z))
        if distance <= (self.radius + other.radius):
            return True
        return False

    def collision(self, other, dt):

        line = self.position - other.position
        line_normalized = line / mag(line)
        COR = (self.COR + other.COR)/2
        distance = dist((self.position.x,self.position.y,self.position.z), (other.position.x,other.position.y,other.position.z))

        if other.is_static:
            overlap_distance = (self.radius + other.radius) - distance
            self.acceleration += line_normalized * overlap_distance * 100

 
        #Legacy
        #Move outside collision range
        #while True:
        #    self.position += line * dt
        #    if self.check_for_collision(other) == False:
        #        break

        #Apply velocity change
        #if other.is_static:
        #    magnitude = mag(self.velocity) / mag(line) * COR
        #    if mag(self.velocity) < 0.5:
        #        magnitude = 0
        #    self.velocity = line * magnitude

    
