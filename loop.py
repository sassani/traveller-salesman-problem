import collections
import heapq as hq

from city import City


class Loop:

    def __init__(self, cities, id):
        self.cities = {}
        self.edges = []
        self.neighbors = {}
        self._size = len(cities)
        self.id = id

        # each city in this circle
        for i in range((self._size)):
            # each neighbor for this city
            cities[i].loop_id = id
            for neighbor in cities[i].neighbors:
                # common is a list of current loop cities wich are in-common in a neighbor
                common = []
                temp = self.neighbors.get(neighbor.id, False)
                if(temp):
                    common = temp

                common.append(cities[i])

                self.neighbors[neighbor.id] = common
            if(i < (self._size)-1):
                self.edges.append([cities[i], cities[i+1]])
                cities[i]._to = cities[i+1]
            self.cities[cities[i].id] = cities[i]
        self.edges.append([cities[(self._size)-1], cities[0]])

        for city in cities:
            self.neighbors.pop(city.id)

    def size(self):
        return self._size

    def find_border(self, other, last_borders):
        # find neighbors of loop1 and its in common cities
        for self_neighbor, cities_incommon in self.neighbors.items():
            for other_city_id, other_city in other.cities.items():
                # check each city on neighbors in loop1 and  cities of loop2
                if(self_neighbor == other_city_id):
                    # add in-common borders between loop1 and loop2
                    for t in cities_incommon:
                        dist = t.sqr_dist_to(other_city)
                        hq.heappush(last_borders, (dist, t, other_city))
        return last_borders
