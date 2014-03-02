# ------------------------------------------------------------------------------- #
# grid_converter.py - Converts a grid map with population to the following format #
# lon, lat, population                                                            #
# Author: Thyago Mota                                                             #
# Date: 02/01/2014                                                                #
# ------------------------------------------------------------------------------- #

import datetime, shapely, sys, math
from datetime import datetime, date, time
from shapely.geometry import Polygon, Point
from math import modf

def help():
	print('Use: ' + sys.argv[0] + ' input_file geometry_file output_file')

# ------------------------------------------------------------------------------- #
# Some definitions                                                                #
# ------------------------------------------------------------------------------- #
FEEDBACK_NUM_RECORDS = 100
NUM_ARGS             = 4
TOLERANCE            = 0.00001
ARCGIS_NO_DATA_VALUE = -3.40282346639e+038

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
print('Trying to open the input and geometry files for reading')
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
	output = open(sys.argv[3], 'wt')
except:
	print('Could not open file ' + sys.argv[3])
	input.close()
	geometry.close()
	exit(4)
print('Success!')

# ------------------------------------------------------------------------------- #
# Reading geometry file                                                           #
# ------------------------------------------------------------------------------- #
print('Reading geometry file')
geoData = []
for line in geometry:
	line = line.replace('\n', '')	
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
# Reading metadata                                                                #
# ------------------------------------------------------------------------------- #
print('Metadata:')
for i in range(0, 6):
	line = input.readline()
	line = line.replace('\n', '')
	line = " ".join(line.split()) # eliminates duplicate whitespaces
	data = line.split(' ')
	#print(data[1])
	if i == 0:
		nCols = int(data[1])
	elif i == 1:
		nRows = int(data[1])
	elif i == 2:
		xllCorner = float(data[1])
	elif i == 3:
		yllCorner = float(data[1])
	elif i == 4:
		cellSize = float(data[1])
	else:
		noDataValue = float(data[1])
print('\tnCols: \t\t' + str(nCols))
print('\tRows: \t\t' + str(nRows))
print('\txllCorner: \t' + str(xllCorner))
print('\tyllCorner: \t' + str(yllCorner))
print('\tcellSize: \t' + str(cellSize))
print('\tnoDataValue: \t' + str(noDataValue))
print('Grid box:')
print('\t(' + str(xllCorner) + ',' + str(yllCorner) + ')')
print('\t(' + str(xllCorner + nCols * cellSize) + ',' + str(yllCorner) + ')')
print('\t(' + str(xllCorner) + ',' + str(yllCorner + nRows * cellSize) + ')')
print('\t(' + str(xllCorner + nCols * cellSize) + ',' + str(yllCorner + nRows * cellSize) + ')')

# ------------------------------------------------------------------------------- #
# Reading the grid                                                                #
# ------------------------------------------------------------------------------- #
grid = [ [ 0. for j in xrange(nCols) ] for i in xrange(nRows) ]
i = 0
totalUnbounded = 0
for line in input:
	line = line.replace('\n', '')
	if line[0] == ' ':
		line = line[1:]
	data = line.split(' ')
	for j in xrange(nCols):
		value = float(data[j])
		if value == ARCGIS_NO_DATA_VALUE or value == noDataValue or value < 0:
			continue
		grid[i][j] = value
		totalUnbounded = totalUnbounded + value
	i = i + 1
input.close()
print('Total unbounded: ' + str(totalUnbounded))

# ------------------------------------------------------------------------------- #
# Writing the new file                                                            #
# ------------------------------------------------------------------------------- #
print('Writing the new file')
totalBounded = 0
for i in xrange(nRows):
	#print('Line ' + str(i+1) + ' of ' + str(nRows))
	lat = yllCorner + (nRows - i) * cellSize + cellSize/2 # cellSize/2 to have values centered instead of top-left
	for j in xrange(nCols):
		if grid[i][j] == 0:
			continue
		lon = xllCorner + j * cellSize + cellSize/2 # cellSize/2 to have values centered instead of top-left
		point = Point(lon, lat)
		if point.within(poly):		
			totalBounded = totalBounded + grid[i][j]
			output.write(str.format('{0:.5f}', lon) + ',' + str.format('{0:.5f}', lat) + ',' + str.format('{0:.2f}', grid[i][j]) + '\n')
output.close()
print('Total bounded: ' + str(totalBounded))
		
# ------------------------------------------------------------------------------- #
# Script ends                                                                     #
# ------------------------------------------------------------------------------- #
endTime = datetime.now()
print('End time: ' + str(endTime.hour) + ':' + str(endTime.minute) + ':' + str(endTime.second)) 
elapsedTime = endTime - startTime
print('Elapsed time: ' + str(elapsedTime))