from particles import *
import util

class Grid:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.width = int(grid_size.x)
        self.lenght = int(grid_size.y)
        self.height = int(grid_size.z)
        self.number_of_wall_particles = 4
        self.offset_between_wall_particles = 0.5
        self.radius_of_wall_particles = 0.5
        self.enclosure = Enclosure(grid_size)
        self.grid = self.create_grid()

    def create_grid(self):
        grid = []
        for i in range(0, self.width):
            plane = []
            for j in range(0, self.lenght):
                row = []
                for k in range(0, self.height):
                    cell = []
                    if i == 0 or j == 0 or k == 0:
                        pos = util.find_position_for_static_wall_particles(i,j,k, vec(self.width-1, self.lenght-1, self.height-1))
                        for p in pos:
                            cell.append(StaticParticle(p,self.radius_of_wall_particles))

                    elif i == self.width-1 or j == self.lenght-1 or k == self.height-1:
                        pos = util.find_position_for_static_wall_particles(i,j,k, vec(self.width-1, self.lenght-1, self.height-1))
                        for p in pos:
                            cell.append(StaticParticle(p,self.radius_of_wall_particles))

                    row.append(cell)
                plane.append(row)
            grid.append(plane)
        return grid

    #Add and move particle in grid
    def update_grid(self, particle):
        x = round(particle.position.x)
        y = round(particle.position.y)
        z = round(particle.position.z)

        old_x = round(particle.last_position.x)
        old_y = round(particle.last_position.y)
        old_z = round(particle.last_position.z)

        if x != old_x or y != old_y or z != old_z: 

            if particle in self.grid[old_x][old_y][old_z]:
                self.grid[old_x][old_y][old_z].remove(particle)

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
                    if self.grid[i][j][k] != []:
                        for p in self.grid[i][j][k]:
                            if p != particle:
                                neighbours.append(p)
        return neighbours

class Enclosure:
    def __init__(self, grid_size):
        self.centre = vector((grid_size.x-1)/2, (grid_size.y-1)/2, (grid_size.z-1)/2)
        self.size = vector((grid_size.x-2), (grid_size.y-2), (grid_size.z-2))
        self.box = box(pos=self.centre, size = self.size, opacity=0.3)