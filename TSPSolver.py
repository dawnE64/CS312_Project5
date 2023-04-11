#!/usr/bin/python3

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT6':
	from PyQt6.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))


import time
import numpy as np
from TSPClasses import *
import heapq
import itertools


class TSPSolver:
	def __init__( self, gui_view ):
		self._scenario = None

	def setupWithScenario( self, scenario ):
		self._scenario = scenario


	''' <summary>
		This is the entry point for the default solver
		which just finds a valid random tour.  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of solution,
		time spent to find solution, number of permutations tried during search, the
		solution found, and three null values for fields not used for this
		algorithm</returns>
	'''
	def defaultRandomTour( self, time_allowance=60.0 ):
		results = {}  # I think this is called a dictionary? It maps strings to values to transfer to the reader.
		cities = self._scenario.getCities()  # gets the cities that have already been generated elsewhere
		ncities = len(cities)
		foundTour = False
		count = 0
		bssf = None
		start_time = time.time()
		while not foundTour and time.time()-start_time < time_allowance:
			# create a random permutation
			perm = np.random.permutation( ncities )  # Just a random shuffle of numbers from 0 to n-1
			route = []  # PATH. We will be adding cities to this in a random order.
			# Now build the route using the random permutation
			for i in range( ncities ):
				route.append( cities[ perm[i] ] )  # PATH. We will be adding cities to this in a random order.
			bssf = TSPSolution(route) # Creates an instance of class TSPSolution with this route which can be used to compute further information
			count += 1
			if bssf.cost < np.inf: # Verify that the cost isn't infinite. If not, then it is valid.
				# Found a valid route
				foundTour = True
		end_time = time.time()
		results['cost'] = bssf.cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results


	''' <summary>
		This is the entry point for the greedy solver, which you must implement for
		the group project (but it is probably a good idea to just do it for the branch-and
		bound project as a way to get your feet wet).  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number of solutions found, the best
		solution found, and three null values for fields not used for this
		algorithm</returns>
	'''
	def greedy( self,time_allowance=60.0 ):
		results = {}  # I think this is called a dictionary? It maps strings to values to transfer to the reader.
		cities = self._scenario.getCities()  # gets the cities that have already been generated elsewhere
		# debug_printAllDistances(cities)
		ncities = len(cities)
		foundTour = False
		bssf = None
		start_time = time.time()
		route = []  # PATH
		visited_cities = set()
		current_city = cities[0]
		# n turns. i is NOT a node id.
		for i in range(ncities):
			visited_cities.add(current_city)
			nearest_city = findNearestCity(current_city, cities, visited_cities)
			if nearest_city is not None:
				route.append(nearest_city)  # Append nearest_city to path
				visited_cities.add(nearest_city)  # Consider nearest_city visited
				current_city = nearest_city  # Set current_city to nearest_city
		route.append(cities[0])
		bssf = TSPSolution(route)  # Creates an TSPSolution for computing information
		if bssf.cost < np.inf:  # Verify that the cost isn't infinite. If not, then it is valid.
			# Found a valid route
			foundTour = True
		end_time = time.time()
		results['cost'] = bssf.cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = 0  # Greedy always returns after the first attempt.
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results


''' <summary>
		returns None if no close cities are found.
'''
def findNearestCity(current_city, cities, visited_cities):
	# Compare all city differences and return the nearest one.
	ncities = len(cities)
	nearest_city = None
	nearest_cost = np.inf
	for i in range(ncities):
		if not visited_cities.__contains__(cities[i]):  # Has next city NOT been visited?
			distance_to_i_city = current_city.costTo(cities[i])
			if distance_to_i_city < nearest_cost:
				nearest_city = cities[i]
				nearest_cost = distance_to_i_city
	return nearest_city


# def debug_printAllDistances(cities):
# 	for i in range(len(cities)):
# 		for j in range(len(cities)):
# 			distance = cities[i].costTo(cities[j])
# 			print(f'dist from {i} to {j}: {distance}')


''' <summary>
		This is the entry point for the branch-and-bound algorithm that you will implement
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number solutions found during search (does
		not include the initial BSSF), the best solution found, and three more ints:
		max queue size, total number of states created, and number of pruned states.</returns>
	'''
def branchAndBound( self, time_allowance=60.0 ):
		# init
		results = {}  # I think this is called a dictionary? It maps strings to values to transfer to the reader.
		cities = self._scenario.getCities()  # gets the cities that have already been generated elsewhere
		ncities = len(cities)
		foundTour = False
		count = 0
		bssf = None
		start_time = time.time()
		# todo loop until hit leaf
		while not foundTour and time.time()-start_time < time_allowance:
			# create a random permutation
			perm = np.random.permutation( ncities )  # Just a random shuffle of numbers from 0 to n-1
			route = []  # PATH. We will be adding cities to this in a random order.
			# Now build the route using the random permutation
			for i in range( ncities ):
				route.append( cities[ perm[i] ] )  # PATH. We will be adding cities to this in a random order.
			bssf = TSPSolution(route) # Creates an instance of class TSPSolution with this route which can be used to compute further information
			count += 1
			if bssf.cost < np.inf: # Verify that the cost isn't infinite. If not, then it is valid.
				# Found a valid route
				foundTour = True
			# todo calc lower bound
			# BELOW IS THE PARTS FOR MY HEAP CLASS
			branchAndBoundHeap = BranchAndBoundHeap()
			'''
			route = []  # PATH
			visited_cities = set()
			current_city = cities[0]
			'''
		# todo handle hitting leaf
		# todo save current bssf
		end_time = time.time()
		results['cost'] = bssf.cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results
		pass


''' <summary>
		This is the entry point for the algorithm you'll write for your group project.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number of solutions found during search, the
		best solution found.  You may use the other three field however you like.
		algorithm</returns>
'''
def fancy( self,time_allowance=60.0 ):
	pass
