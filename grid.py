from particles import *
import util

class Grid:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.radius_of_wall_particles = 0.75

        self.grid = self.create_grid()
        self.spawn_grid_bounds()
        self.drawGrid()

    def create_grid(self):
        grid = []
        for i in range(0, round(self.grid_size.x)):
            plane = []
            for j in range(0, round(self.grid_size.y)):
                row = []
                for k in range(0, round(self.grid_size.z)):
                    cell = []
                    row.append(cell)
                plane.append(row)
            grid.append(plane)
        return grid
    
    def spawn_grid_bounds(self):
        #The bounds is a hollow cuboid made of static particles.
        for i in range(0, round(self.grid_size.x)):
            for j in range(0, round(self.grid_size.y)):
                for k in range(0, round(self.grid_size.z)):
                    if i == 0 or j == 0 or k == 0:
                        sp = StaticParticle(vec(i,j,k),self.radius_of_wall_particles)
                        self.grid[i][j][k].append(sp)

                    elif i == self.grid_size.x-1 or j == self.grid_size.y-1 or k == self.grid_size.z-1:
                        sp = StaticParticle(vec(i,j,k),self.radius_of_wall_particles)
                        self.grid[i][j][k].append(sp)
        


    #Add or move particle in grid
    def update_grid(self, particle):

        if util.grid_place_has_changed(particle.position, particle.last_position): 

            x_old = round(particle.last_position.x)
            x_old = round(particle.last_position.y)
            x_old = round(particle.last_position.z)

            x = round(particle.last_position.x)
            y = round(particle.last_position.y)
            z = round(particle.last_position.z)

            if x < 0 or y < 0 or z < 0 or x >= self.grid_size.x-1 or y >= self.grid_size.y-1 or z >= self.grid_size.z-1:
                particle.position = vec(2,2,2)
                particle.velocity = vec(0,0,0)
                print("Particle out of bounds")

            if particle in self.grid[x_old][x_old][x_old]:
                self.grid[x_old][x_old][x_old].remove(particle)

            self.grid[x][y][z].append(particle)

    #Return array of neighbouring particles (according to the grid) of the particle
    def get_particles_in_neighbourhood(self, particle):
        x = round(particle.position.x)
        y = round(particle.position.y)
        z = round(particle.position.z)

        neighbours = []
        for i in range(x-1,x+2):
            for j in range(y-1, y+2):
                for k in range(z-1,z+2):
                    if i <= self.grid_size.x-1 and j <= self.grid_size.y-1 and k <= self.grid_size.z-1 and i >= 0 and j >= 0 and k >= 0:
                        if self.grid[i][j][k] != []:
                            for p in self.grid[i][j][k]:
                                if p != particle:
                                    neighbours.append(p)
        return neighbours


    def drawGrid(self):
        self.centre = vector((self.grid_size.x-1)/2, (self.grid_size.y-1)/2, (self.grid_size.z-1)/2)
        self.size = vector((self.grid_size.x-2), (self.grid_size.y-2), (self.grid_size.z-2))
        self.box = box(pos=self.centre, size = self.size, opacity=0.3)