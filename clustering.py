# ------------------------------------------------------------------------------- #
# clustering.py - Runs a clustering algorithm (DBSCAN) to identify cell towers    #
#                 in Abidjan area that are close to each other; assign a new      #
#                 coordinate to each cluster to be the centroid location          #
# Author: Thyago Mota                                                             #
# Date: 01/24/2014                                                                #
# ------------------------------------------------------------------------------- #

import datetime, math
from datetime import datetime, date, time

# ------------------------------------------------------------------------------- #
# Calculates the centroid of a set of points                                      #
# points = [ (lon, lat), ... ]                                                    #
# ------------------------------------------------------------------------------- #
def centroid(points):
	sumLon = 0
	sumLat = 0
	total  = 0
	for point in points:
		sumLon = sumLon + point[0]
		sumLat = sumLat + point[1]
		total = total + 1
	return [ sumLon / total, sumLat / total ]

# ------------------------------------------------------------------------------- #
# haversine function that calculates the distance (in km) between two points      #
# ------------------------------------------------------------------------------- #
def haversine( XY ):
	p1 = [ x * ( math.pi / 180 ) for x in XY[0] ]
	p2 = [ x * ( math.pi / 180 ) for x in XY[1] ]
	d_lon = p1[0] - p2[0]
	d_lat = p1[1] - p2[1]
	h = (math.sin(d_lat/2))**2 + math.cos(p1[1]) * math.cos(p2[1]) * (math.sin(d_lon/2))**2
	return 6372.8 * 2 * math.atan2( math.sqrt(h), math.sqrt(1-h) )

# ------------------------------------------------------------------------------- #
# neighboors function that identifies locations that are nearby                   #
# ------------------------------------------------------------------------------- #
def neighboors(tower, towers, eps):
	neighboors = []
	for candidate in towers:
		if candidate == tower:
			continue
		d = haversine([towers[candidate], towers[tower]])
		if d <= eps:
			neighboors.append(candidate)
	return neighboors

# ------------------------------------------------------------------------------- #
# DBSCAN clustering algorithm                                                     #
# ------------------------------------------------------------------------------- #	
def dbscan(towers, eps, min):
	clusters = []
	visited = {}
	for tower in towers:
		visited[tower] = False
	for tower in towers:
		if visited[tower]:
			continue
		visited[tower] = True
		# print( 'Visiting ' + str( tower ) )
		n = neighboors(tower, towers, eps)	
		# print( 'Neighboors of ' + str( tower ) + ': ' + str( n ) )
		if len(n) >= min:			
			newCluster = [tower]
			# expand neighboor list
			for other in n:
				visited[other] = True
				nn = neighboors(other, towers, eps)
				# print( nn )
				if len(nn) >= min:
					n = n + nn
			n = list(set(n))
			# print( 'Expanded neighboors of ' + str( tower ) + ': ' + str( n ) )
			# add neighboors IF they are not in a cluster
			for other in n:
				if other == tower:
					continue
				found = False
				for c in clusters:
					if other in c:
						found = True
						break
				if not found:
					newCluster.append(other)
					visited[other] = True # no need to revisit a location that is already in a cluster
			# print(newCluster)
			clusters.append(newCluster)
	return clusters

# ------------------------------------------------------------------------------- #
# Some definitions                                                                #
# ------------------------------------------------------------------------------- #
DATA_FOLDER  = 'd:\\development\\research\\data\\'
D4D_FOLDER   = 'D4D\\'
TOWERS_FILE  = 'abidjan_towers.csv'
LOCAL_FOLDER = '..\\data\\'
OUTPUT_FILE  = 'clusters.csv'
# DBSCAN parameters
EPSILON      = 0.5 # km
MIN_POINTS   = 1

# ------------------------------------------------------------------------------- #
# Script begins                                                                   #
# ------------------------------------------------------------------------------- #
startTime = datetime.now()
print('Start time: ' + str(startTime.hour) + ':' + str(startTime.minute) + ':' + str(startTime.second)) 

# ------------------------------------------------------------------------------- #
# Reading Abidjan cell towers                                                     #
# towers[cellID] = (lon, lat)                                                     #
# ------------------------------------------------------------------------------- #
print('Reading Abidjan cell towers')
file = open(DATA_FOLDER + D4D_FOLDER + TOWERS_FILE, 'rt')
towers = {}
for line in file:
	line   = line.replace('\n', '')	
	data   = line.split(',')		
	tower  = int(data[0])
	lon    = float(data[1])
	lat    = float(data[2])
	towers[tower] = (lon, lat)
file.close()
print(str(len(towers)) + ' towers read')

# ------------------------------------------------------------------------------- #
# Running the clustering procedure                                                #
# ------------------------------------------------------------------------------- #
clusters = dbscan(towers, EPSILON, MIN_POINTS)
# exclude clusters with just one tower
clusters = [cluster for cluster in clusters if len(cluster) > 1]	
print(str(len(clusters)) + ' clusters created')

# ------------------------------------------------------------------------------- #
# Printing cluster information                                                    #
# ------------------------------------------------------------------------------- #
output = open(LOCAL_FOLDER + OUTPUT_FILE, 'wt')
seq = 0
total = 0
for cluster in clusters:
	points = []
	total = total + len(cluster)
	#print(cluster)
	for tower in cluster:
		points.append(towers[tower])
	center = centroid(points)
	output.write(str(seq) + ',' + str(center[0]) + ',' + str(center[1]))
	for tower in cluster:
		output.write(',' + str(tower))
	output.write('\n')
	seq = seq + 1
output.close()
print('Towers in cluster: ' + str(total))
print('New number of venues: ' + str(len(towers) - total + len(clusters)))
	
# ------------------------------------------------------------------------------- #
# Script ends                                                                     #
# ------------------------------------------------------------------------------- #
endTime = datetime.now()
print('End time: ' + str(endTime.hour) + ':' + str(endTime.minute) + ':' + str(endTime.second)) 
elapsedTime = endTime - startTime
print('Elapsed time: ' + str(elapsedTime))