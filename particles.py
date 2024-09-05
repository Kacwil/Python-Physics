from vpython import *
import util

class StaticParticle:
    def __init__(self, position=vec(2,2,2), radius=0.5, visible=False, COR=0.5):
        self.position = position
        self.radius = radius
        self.is_static = True
        self.COR = COR #Coefficient of restituion

        if visible:
            self.drawSphere()

    def drawSphere(self):
        self.sphere = sphere(pos=self.position, radius=self.radius, color=vec(1,0,0), opacity=0.3)

class StaticCuboid(StaticParticle):
    def __init__(self, position=vec(2, 2, 2), radius=0.5, visible=False, COR=0.5):
        super().__init__(position, radius, visible, COR)




class DynamicParticle(StaticParticle):
    def __init__(self, position=vec(2,2,2), velocity=vec(0,0,0), acceleration=vec(0,0,0), mass=1 ,radius=0.5, visible=True, COR=0.5, label=False, id=None):
        super().__init__(position, radius, visible, COR)

        self.id = id
        self.is_static = False
        self.last_position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.mass = mass

        self.has_label = False
        self.label = None


    def drawSphere(self):
        self.sphere = sphere(pos=self.position, radius=self.radius, color=vec(random(),random(),random()))
    
    
    def update_particle(self, dt, grid):

        self.physics_update(dt)
        self.grid_update(grid)

        for neighbour in grid.get_particles_in_neighbourhood(self):
            if self.check_for_collision(neighbour):
                self.handle_collision(neighbour,dt)

    def physics_update(self, dt):

        #Gravity and Drag
        #self.acceleration += util.physics_gravity()
        #self.acceleration += util.physics_air_drag(self.velocity, self.mass)

        self.last_position = self.position
        self.velocity = self.velocity + dt * self.acceleration
        self.acceleration = vec(0,0,0) #Reset acceleration
        self.position = self.position + dt * self.velocity
        self.sphere.pos = self.position

    def grid_update(self, grid):
        if util.grid_place_has_changed(self.position, self.last_position):
            grid.update_grid(self)

    def check_for_collision(self, other):
        distance = dist((self.position.x,self.position.y,self.position.z), (other.position.x,other.position.y,other.position.z))
        if distance <= (self.radius + other.radius):
            return True
        return False

    def handle_collision(self, other, dt):

        line = self.position - other.position
        line_normalized = line / mag(line)
        COR = (self.COR + other.COR)/2
        distance = dist((self.position.x,self.position.y,self.position.z), (other.position.x,other.position.y,other.position.z))

        if other.is_static:
            overlap_distance = (self.radius + other.radius) - distance
            self.acceleration += line_normalized * 10000 * overlap_distance / self.mass # F = kx^2
            self.velocity = self.velocity * .999

        if other.is_static == False:
            overlap_distance = (self.radius + other.radius) - distance
            self.acceleration += line_normalized * 10000 * overlap_distance / self.mass
            self.velocity = self.velocity * .999


    
