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
        if mag(line) != 0:
            line_normalized = line / mag(line)
        else:
            line_normalized = vec(0,0,0)
        COR = (self.COR + other.COR)/2
        distance = dist((self.position.x,self.position.y,self.position.z), (other.position.x,other.position.y,other.position.z))

        overlap_distance = (self.radius + other.radius) - distance
        self.acceleration += line_normalized * 10000 * overlap_distance * dt / self.mass # F = kx^2
        self.velocity = self.velocity * .999

        



class Spring():
    def __init__(self, particle1, particle2, lenght):
        self.p1 = particle1
        self.p2 = particle2
        self.lenght = lenght   
        self.spring_constant = 10000
        self.spring_friction = 0
        self.curve = curve(pos=[self.p1.position, self.p2.position])

    def update(self, dt):
        
        line = self.p1.position - self.p2.position
        line_normalized = line / mag(line)
        distance = dist((self.p1.position.x,self.p1.position.y,self.p1.position.z), (self.p2.position.x,self.p2.position.y,self.p2.position.z))



        if distance > self.lenght:
            x = distance - self.lenght
            if not self.p1.is_static:
                self.p1.acceleration += -line_normalized * self.spring_constant * x * dt / self.p1.mass # F = kx^2
                self.p1.velocity = self.p1.velocity * (1 - self.spring_friction)
            if not self.p2.is_static:
                self.p2.acceleration += line_normalized * self.spring_constant * x * dt / self.p2.mass # F = kx^2
                self.p2.velocity = self.p2.velocity * (1 - self.spring_friction)


        if distance < self.lenght:
            x = distance - self.lenght
            if not self.p1.is_static:
                self.p1.acceleration += -line_normalized * self.spring_constant * x * dt / self.p1.mass # F = kx^2
                self.p1.velocity = self.p1.velocity * (1 - self.spring_friction)
            if not self.p2.is_static:
                self.p2.acceleration += line_normalized * self.spring_constant * x * dt / self.p2.mass # F = kx^2
                self.p2.velocity = self.p2.velocity * (1 - self.spring_friction)

        self.update_curve()

    def update_curve(self):
        self.curve.modify(0, pos=self.p1.position)
        self.curve.modify(1, pos=self.p2.position)

        distance = dist((self.p1.position.x,self.p1.position.y,self.p1.position.z), (self.p2.position.x,self.p2.position.y,self.p2.position.z))

        if distance > self.lenght:
            self.curve.modify(0, color=vec(0,0,255))
        else:
            self.curve.modify(0, color=vec(0,255,0))




