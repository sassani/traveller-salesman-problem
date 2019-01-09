import math
import sys

from map import Map

TRY_NUMBER = int(sys.argv[1])


min_distanc = math.inf
map_id = -1
for i in range(TRY_NUMBER):

    print('\nItteration: ',str(i+1),'/',str(TRY_NUMBER))

    city_map = Map('cities.csv', int(sys.argv[2]))

    loop_num = len(city_map._loops)
    # city_map.print_loops()

    # print('Number of loops:'+str(loop_num))
    if(loop_num == 1):
        print('End of processing ...')
    else:
        city_map.merge_loops()

    # city_map.print_path()
    result = city_map.save_paths('results/map_'+str(i)+'.txt')
    if(result['totalDist'] < min_distanc):
        min_distanc = result['totalDist']
        map_id = i

f = open('Summary.txt', "w")
f.write('Summary')
f.write('\nmap_id:'+str(map_id))
f.write('\nminimum distance:'+str(min_distanc))
