import copy
import heapq as hq
import os
from pprint import pprint

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from networkx.algorithms import bipartite
from scipy.spatial import Voronoi, voronoi_plot_2d

from city import City
from loop import Loop
from unionfind import UnionFind

DATA_LIMIT = 20


class Map:
    # cities = {}
    # _loops = []
    # _borders = []
    # loops = UnionFind()
    # _print: bool = False

    def __init__(self, cities_data, print: bool = False):
        self.cities = {}
        self._loops = []
        self._borders = []
        self.loops = UnionFind()
        limit = DATA_LIMIT
        self._print = print
        df = pd.read_csv(cities_data)
        upper = len(df)
        if limit != 0:
            upper = limit
        df = df[0:upper]

        for row in df.iterrows():
            city = City(row[1].CityId, row[1].X, row[1].Y)
            self.cities[city.id] = city
        self._create_loops()

    def _create_loops(self):
        points = []
        g_cities = nx.DiGraph()

        for city in self.cities:
            city = self.cities.get(city)
            g_cities.add_node('f-'+str(city.id), bipartite=0)
            g_cities.add_node('t-'+str(city.id), bipartite=1)
            points.append([city.x, city.y])
        points = np.array(points)
        vor = Voronoi(points, incremental=True)

        for point in vor.ridge_points:
            self.cities[point[0]].add_neighbor(self.cities[point[1]])
            self.cities[point[1]].add_neighbor(self.cities[point[0]])
            g_cities.add_edge(
                'f-'+str(self.cities[point[0]]), 't-'+str(self.cities[point[1]]))
            g_cities.add_edge(
                'f-'+str(self.cities[point[1]]), 't-'+str(self.cities[point[0]]))

        temp = bipartite.maximum_matching(g_cities)
        islands = nx.DiGraph()
        i = 0
        for key, value in temp.items():
            # connect cities ...
            self.cities[int(key[2:])].connect_to(self.cities[int(value[2:])])
            islands.add_edge(
                self.cities[int(key[2:])], self.cities[int(value[2:])])
            i += 1
            if(i >= temp.__len__()/2):
                break
        for i, c in enumerate(nx.recursive_simple_cycles(islands)):
        # for i, c in enumerate(nx.simple_cycles(islands)):
            loop = Loop(c, i)
            self._loops.append(loop)
            self.loops.add(i)

        # plt.subplot(121)
        # nx.draw(islands, with_labels=True)
        # plt.savefig('temp_diagram.png')
        # plt.show()

    def loops_borders(self):
        temp_h = []
        n = len(self.loops)
        for i in range(n):
            for j in range(i+1, n):
                temp_h = self._loops[i].find_border(self._loops[j], temp_h)
        return temp_h

    def merge_loops(self):
        city_pairs = self.loops_borders()
        while(city_pairs.__len__() > 0):
            cp = hq.heappop(city_pairs)
            if(not(self.loops.connected(cp[1].loop_id, cp[2].loop_id))):
                # connect loops
                if(self.merge_node(cp[1], cp[2])):
                    self.loops.union(cp[1].loop_id, cp[2].loop_id)

    def merge_node(self, c1: City, c2: City):
        p = c1
        q = c2
        if(self.is_revers(c1, c2)):
            p = c2
            q = c1
        self.connect(q.prev, p.next)
        self.connect(p, q)
        return True

    def connect(self, p: City, q: City)-> bool:
        p.next = q
        q.prev = p
        if(self._print):
            print(str(p.id)+' --> '+str(q.id))

    def is_revers(self, c1: City, c2: City):
        dist_12 = c2.prev.sqr_dist_to(c1.next)
        dist_21 = c1.prev.sqr_dist_to(c2.next)
        return dist_12 > dist_21

    def print_loops(self):
        print('loops ...')
        for loop in self._loops:
            print('------------')
            for vertex in loop.cities:
                print(str(loop.cities.get(vertex))+'\tEnergy: ' +
                      str(loop.cities.get(vertex).energy))

    def print_path(self):
        current_city = self.cities[0]
        current_energy = 10
        dist = 0
        min_enrg = 10
        while True:
            d = current_city.dist_to(current_city.next)
            if(min_enrg > current_energy):
                min_enrg = current_energy
            if(current_energy <= 0):
                d = d * 1.1
            dist += d
            print(str(current_city.id))
            # print(str(current_city.id)+'\tE: '+str(current_energy))
            current_city = current_city.next
            if(current_city.next == self.cities[0]):
                print(current_city.id)
                break
            current_energy += -1
            if(current_city.is_prime):
                current_energy = 10
        print('Distance: '+str(dist))
        print('Minimum Energy:'+str(min_enrg))

    def save_path(self, file_name: str = "myFile.csv"):
        f = open(file_name, "w")
        f.write('Path\n')
        current_city = self.cities[0]
        while True:
            f.write(str(current_city.id)+'\n')
            current_city = current_city.next
            if(current_city.next == self.cities[0]):
                f.write(str(current_city.id)+'\n')
                break
        f.write('0\n')

    def save_paths(self, file_name: str = "myFile.csv"):
        f = open(file_name, "w")
        f.write('Path\n')
        current_city = self.cities[0]
        current_energy = 10
        dist = 0
        min_enrg = 10
        while True:
            d = current_city.dist_to(current_city.next)
            if(min_enrg > current_energy):
                min_enrg = current_energy
            if(current_energy <= 0):
                d = d * 1.1
            dist += d
            f.write(str(current_city.id)+'\n')
            current_city = current_city.next
            if(current_city.next == self.cities[0]):
                f.write(str(current_city.id)+'\n')
                break
            current_energy += -1
            if(current_city.is_prime):
                current_energy = 10
        f.write('0\n')
        print('Distance: '+str(dist))
        return {'totalDist': dist, 'minEnergy': min_enrg}
