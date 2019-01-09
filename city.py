import math
from check_prime import *


class City:
    energy = 0

    def __init__(self, id, x, y):
        self.id = int(id)
        self.x = x
        self.y = y
        self.is_prime = check_prime(id)
        self.neighbors = []
        self.next = City
        self.prev = City
        self.loop_id = -1
        # self.energy = 10

    def __lt__(self, other):
        return self.energy - other.energy

    def sqr_dist_to(self, other):
        return (self.x-other.x)**2 + (self.y-other.y)**2
    
    def dist_to(self, other):
        return math.sqrt((self.x-other.x)**2 + (self.y-other.y)**2)

    def __str__(self):
        return str('{0:d}'.format(int(self.id)))

    def add_neighbor(self, city):
        self.neighbors.append(city)

    def set_loop_id(self, id):
        self.loop_id = id

    def connect_to(self, other):
        self.next = other
        other.prev = self
        if(self.prev):
            self.energy = self.prev.energy-1
        if(self.is_prime):
            self.energy = 10
