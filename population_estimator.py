# ------------------------------------------------------------------------------- #
# population_estimator.py - Estimates populations using cell tower Voronoi polys  #
# cell_id, population                                                             #
# Author: Santiago Gonzalez                                                       #
# Date: April 2014                                                                #
# ------------------------------------------------------------------------------- #

import datetime, shapely, sys, math
from datetime import datetime, date, time
from shapely.geometry import Polygon, Point
from collections import defaultdict
from math import modf

def help():
  print('Usage: ' + sys.argv[0] + ' polygon_file geometry_file grid_population_file output_file')

# ------------------------------------------------------------------------------- #
# Some definitions                                                                #
# ------------------------------------------------------------------------------- #
NUM_ARGS             = 5

# ------------------------------------------------------------------------------- #
# Script begins                                                                   #
# ------------------------------------------------------------------------------- #
startTime = datetime.now()
print('Start time: ' + str(startTime.hour) + ':' + str(startTime.minute) + ':' + str(startTime.second))

# ------------------------------------------------------------------------------- #
# Command line validation                                                         #
# Parameters (required): input_file output_file                                   #
# ------------------------------------------------------------------------------- #
if len(sys.argv) != NUM_ARGS:
  help()
  exit(1)

# ------------------------------------------------------------------------------- #
# Opening of files                                                                #
# ------------------------------------------------------------------------------- #
print('Trying to open the polygon and geometry files for reading')
try:
  input = open(sys.argv[1], 'rt')
except:
  print('Could not open file ' + sys.argv[1])
  exit(2)
try:
  geometry = open(sys.argv[2], 'rt')
except:
  print('Could not open file ' + sys.argv[2])
  input.close()
  exit(3)
try:
  populations = open(sys.argv[3], 'rt')
except:
  print('Could not open file ' + sys.argv[3])
  input.close()
  exit(4)
try:
  output = open(sys.argv[4], 'wt')
except:
  print('Could not open file ' + sys.argv[3])
  input.close()
  geometry.close()
  exit(5)
print('Success!')

# ------------------------------------------------------------------------------- #
# Reading geometry file                                                           #
# ------------------------------------------------------------------------------- #
print('Reading geometry file')
geoData = []
for line in geometry:
  line = line.strip()
  data = line.split(' ')
  for i in range(0, len(data)):
    d = data[i].split(',')
    geoData.append([float(d[0]), float(d[1])])
geometry.close()
print('Geometry file looking good :-)')
#print(geoData)

# ------------------------------------------------------------------------------- #
# Creating a polygon based on geometry                                            #
# ------------------------------------------------------------------------------- #
print('Creating a polygon based on geometry')
poly = Polygon(geoData)
print('That was easy!')

# ------------------------------------------------------------------------------- #
# Load populations into array                                                     #
# ------------------------------------------------------------------------------- #
print('Reading gridded populations')
populationData = {} # map of x,y tuple to number
for line in populations:
  line = line.strip()
  data = line.split(',')
  populationData[(float(data[0]), float(data[1]))] = float(data[2])
populations.close();
print('Finished loading gridded populations')

# ------------------------------------------------------------------------------- #
# Load polygons into array                                                        #
# ------------------------------------------------------------------------------- #
print('Reading polygons')
voronoiPolygons = {} # map of cell tower id to polygon
for line in input:
  line = line.strip()
  data = line.split(',')
  voronoiPolygons.setdefault(int(data[0]),[]).append([float(data[1]), float(data[2])])
for k in voronoiPolygons:
  poly = Polygon(voronoiPolygons[k])
  voronoiPolygons[k] = poly
print('Finished reading polygons')

# ------------------------------------------------------------------------------- #
# Estimate populations                                                            #
# ------------------------------------------------------------------------------- #
print('Estimating...')
estimatedPopulations = defaultdict(int) # map of cell tower id to number, defaultdict ensures values default to 0
for coord in populationData:
    for towerid in voronoiPolygons: # if we aren't deleting used items as we go along, this for loop should be the innermost one, for efficiency
        popAtCoord = populationData[coord]
        point = Point(coord[0], coord[1])
        if point.within(voronoiPolygons[towerid]):
            estimatedPopulations[towerid] += popAtCoord
        #    del populationData[coord] # we can delete this popData entry since it will not appear again

# ------------------------------------------------------------------------------- #
# Writing the new file                                                            #
# ------------------------------------------------------------------------------- #
print('Writing the new file')
for towerid in estimatedPopulations:
    output.write(str.format('{0:.0f}', towerid) + ',' + str.format('{0:.2f}', estimatedPopulations[towerid]) + '\n')
output.close()
print('Finished!')

# ------------------------------------------------------------------------------- #
# Script ends                                                                     #
# ------------------------------------------------------------------------------- #
endTime = datetime.now()
print('End time: ' + str(endTime.hour) + ':' + str(endTime.minute) + ':' + str(endTime.second))
elapsedTime = endTime - startTime
print('Elapsed time: ' + str(elapsedTime))
