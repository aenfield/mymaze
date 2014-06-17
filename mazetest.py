#!/usr/bin/env python
# encoding: utf-8
"""
mazetest.py

Created by Andrew Enfield on 2007-12-27.
Copyright (c) 2007 __MyCompanyName__. All rights reserved.
"""

import unittest

from maze import *


class MazeTest(unittest.TestCase):
	def setUp(self):
		pass
		
	def testCreateSmallMaze(self):
		m = Maze(2,3)
		self.assertEqual(3, m.width)
		self.assertEqual(2, m.height)
		
	def testMazeHasBasicCells(self):
		m = Maze(2,3)
		self.assertEqual(2, len(m.cells))
		self.assertEqual(3, len(m.cells[0]))
		self.assertEqual(3, len(m.cells[1]))

	def testSmallMazeStringRepresentaiton(self):
		expected = \
""" ___ 
|_|_|
|_|_|
"""
		m = Maze(2,2)
		s = str(m)
		self.assertEqual(expected, s)

	def testABitBiggerMazeStringRepresentation(self):
		expected = \
""" _______ 
|_|_|_|_|
|_|_|_|_|
|_|_|_|_|
|_|_|_|_|
"""
		m = Maze(4,4)
		s = str(m)
		self.assertEqual(expected, s)

	def testUnevenMazeStringRepresentation(self):
		expected = \
""" _______ 
|_|_|_|_|
|_|_|_|_|
"""
		m = Maze(2,4)
		s = str(m)
		self.assertEqual(expected, s)

	def testHorizontalPassagesShowInSimpleMaze(self):
		expected = \
""" ___ 
|___|
|_|_|
"""
		m = Maze(2,2)
		# we manually carve the east wall of cell 0,0 and the west wall of cell
		# 0,1
		m.cells[0][0].walls[east] = passage
		m.cells[0][1].walls[west] = passage 
		s = str(m)
		self.assertEqual(expected, s)
		
	def testVerticalPassagesShowInSimpleMaze(self):
		expected = \
""" ___ 
| |_|
|_|_|
"""
		m = Maze(2,2)
		# we manually carve the south wall of cell 0,0 and the north wall of cell
		# 1,0
		m.cells[0][0].walls[south] = passage
		m.cells[1][0].walls[north] = passage 
		s = str(m)
		self.assertEqual(expected, s)

	def testHorzAndVertPassagesShowInSimpleMaze(self):
		expected = \
""" ___ 
|_| |
|___|
"""
		m = Maze(2,2)
		# we manually carve the south wall of cell 0,1 / north wall of cell 1,1 and
		# the east wall of 1,0 / west wall of 1,1
		m.cells[0][1].walls[south] = passage
		m.cells[1][1].walls[north] = passage
		m.cells[1][0].walls[east] = passage
		m.cells[1][1].walls[west] = passage
		s = str(m)
		self.assertEqual(expected, s)
		
		
	def testDirectionsEnumExists(self):
		self.assertEqual(0, north)
		self.assertEqual(1, east)
		self.assertEqual(2, south)
		self.assertEqual(3, west)
		
	def testCellEdgeEnumExists(self):
		self.assertEqual(0, wall)
		self.assertEqual(1, permanentwall)		# can't be carved through - like the edge of the maze
		self.assertEqual(2, passage)
		
	def testCellsHaveWalls(self):
		m = Maze(2,2) 
		c = m.cells[0][0]
		self.assertEqual(wall, c.walls[east])
		self.assertEqual(wall, c.walls[south])
		
	def testCellsAtEdgeHavePermanentWalls(self):
		m = Maze(2,2)
		self.assertEqual(permanentwall, m.cells[0][0].walls[north])
		self.assertEqual(permanentwall, m.cells[0][0].walls[west])
		self.assertEqual(permanentwall, m.cells[1][0].walls[west])
		self.assertEqual(permanentwall, m.cells[1][0].walls[south])
		self.assertEqual(permanentwall, m.cells[1][1].walls[east])
		self.assertEqual(permanentwall, m.cells[1][1].walls[south])
		self.assertEqual(permanentwall, m.cells[0][1].walls[north])
		self.assertEqual(permanentwall, m.cells[0][1].walls[east])
		
	def testReverseOfDirection(self):
		self.assertEqual(east, Maze.reverseOf(west))
		self.assertEqual(west, Maze.reverseOf(east))
		self.assertEqual(south, Maze.reverseOf(north))
		self.assertEqual(north, Maze.reverseOf(south))
		
	def testCellPositionToOrdinal(self):
		m = Maze(3,4)
		self.assertEqual(0, m.cellPositionToOrdinal(0,0))
		self.assertEqual(5, m.cellPositionToOrdinal(1,1))
		self.assertEqual(11, m.cellPositionToOrdinal(2,3))
		
	def testOrdinalToCellPosition(self):
		m = Maze(3,4)
		self.assertEqual((0,0), m.ordinalToCellPosition(0))
		self.assertEqual((1,1), m.ordinalToCellPosition(5))
		self.assertEqual((2,3), m.ordinalToCellPosition(11))
		
	def testOrdinalToCell(self):
		m = Maze(3,4)
		self.assertEqual(m.cells[0][0], m.ordinalToCell(0))
		self.assertEqual(m.cells[2][3], m.ordinalToCell(11))

	def testStartAndFinishCells(self):
		m = Maze(3,4)
		self.assertEqual(m.cells[0][0], m.startCell)
		self.assertEqual(m.cells[2][3], m.finishCell)


class CellTest(unittest.TestCase):
	def testCreateSimpleCell(self):
		c = Cell(0, 0)

	def testCellStringRepresentation(self):
		c = Cell(0, 0)					# by default the cell has all four walls
		self.assertEqual(str(c), '_|')
		
		c.walls[east] = passage
		self.assertEqual(str(c), '__')
		
		c.walls[east] = wall			# add the east wall back in to test bottom passage only
		c.walls[south] = passage
		self.assertEqual(str(c), ' |')
		
		c.walls[east] = passage			# and knock the east wall back out again to test both
		self.assertEqual(str(c), ' _') 

	def testCellReprRepresentation(self):
		c = Cell(0, 0)
		self.assertEqual('<Cell at [0][0]>', repr(c))

	def testSingleSimpleAdjacentCell(self):
		m = Maze(2,2)
		c = m.cells[0][0]
		self.assertEqual(m.cells[0][1], c.getAdjacentCell(east))
		
	def testManyAdjacentCells(self):
		m = Maze(3,3)
		c = m.cells[1][1]
		self.assertEqual(m.cells[0][1], c.getAdjacentCell(north))
		self.assertEqual(m.cells[1][2], c.getAdjacentCell(east))
		self.assertEqual(m.cells[2][1], c.getAdjacentCell(south))
		self.assertEqual(m.cells[1][0], c.getAdjacentCell(west))

	def testAdjacentCellReturnsNoneAtEdgeOfMaze(self):
		m = Maze(3,3)
		c1 = m.cells[0][1]
		self.assertEqual(None, c1.getAdjacentCell(north))
		c2 = m.cells[1][0]
		self.assertEqual(None, c2.getAdjacentCell(west))

	def testGetDirectionOfAdjacentCell(self):
		m = Maze(3,3)
		c = m.cells[1][1]
		self.assertEqual(north, c.getDirectionOfAdjacentCell(m.cells[0][1]))
		self.assertEqual(west, c.getDirectionOfAdjacentCell(m.cells[1][0]))
		self.assertEqual(east, c.getDirectionOfAdjacentCell(m.cells[1][2]))
		self.assertEqual(south, c.getDirectionOfAdjacentCell(m.cells[2][1]))

	def testCellToOrdinal(self):
		m = Maze(3,4)
		self.assertEqual(0, m.cells[0][0].ordinal())
		self.assertEqual(5, m.cells[1][1].ordinal())
		self.assertEqual(11, m.cells[2][3].ordinal())

	def testIsCellPositionInMaze(self):
		m = Maze(3,3)
		self.assertEqual(True, m.isCellPositionInMaze(0, 0))
		self.assertEqual(True, m.isCellPositionInMaze(2, 2))
		self.assertEqual(False, m.isCellPositionInMaze(-1, 0))
		self.assertEqual(False, m.isCellPositionInMaze(0, -1))
		self.assertEqual(False, m.isCellPositionInMaze(0, 3))
		self.assertEqual(False, m.isCellPositionInMaze(3, 0))

	def testOpenPassageByDirection(self):
		m = Maze(2,2)
		c = m.cells[0][0]
		c.openPassageInDirection(east)
		self.assertEqual(passage, c.walls[east])
		self.assertEqual(passage, m.cells[0][1].walls[west])

	def testOpenMultiplePassagesByDirection(self):
		m = Maze(3,3)
		c = m.cells[1][1]
		for direction in directions:
			c.openPassageInDirection(direction)
		self.assertEqual(passage, c.walls[north])
		self.assertEqual(passage, c.walls[south])
		self.assertEqual(passage, c.walls[east])
		self.assertEqual(passage, c.walls[west])
		self.assertEqual(passage, m.cells[0][1].walls[south])
		self.assertEqual(passage, m.cells[1][0].walls[east])
		self.assertEqual(passage, m.cells[1][2].walls[west])
		self.assertEqual(passage, m.cells[2][1].walls[north])

	def testOpenPassageToSpecifiedCell(self):
		m = Maze(3,3)
		c = m.cells[1][1]
		c.openPassageToCell(m.cells[1][2])
		self.assertEqual(passage, c.walls[east])
		self.assertEqual(passage, m.cells[1][2].walls[west])

	def testOpenMultiplePassagesUsingAdjacentCells(self):
		m = Maze(3,3)
		c = m.cells[1][1]
		c.openPassageToCell(m.cells[0][1])
		c.openPassageToCell(m.cells[1][2])
		c.openPassageToCell(m.cells[2][1])
		c.openPassageToCell(m.cells[1][0])
		self.assertEqual(passage, c.walls[north])
		self.assertEqual(passage, c.walls[south])
		self.assertEqual(passage, c.walls[east])
		self.assertEqual(passage, c.walls[west])
		self.assertEqual(passage, m.cells[0][1].walls[south])
		self.assertEqual(passage, m.cells[1][0].walls[east])
		self.assertEqual(passage, m.cells[1][2].walls[west])
		self.assertEqual(passage, m.cells[2][1].walls[north])
		
	def testGetAdjacentCells(self):
		m = Maze(3,3)
		adjCells = m.cells[0][0].getAllAdjacentCells()
		self.assertEqual(2, len(adjCells))
		self.assert_(m.cells[1][0] in adjCells)
		self.assert_(m.cells[0][1] in adjCells)
		adjCells = m.cells[1][1].getAllAdjacentCells()
		self.assertEqual(4, len(adjCells))
		self.assert_(m.cells[1][0] in adjCells)
		self.assert_(m.cells[0][1] in adjCells)
		self.assert_(m.cells[1][2] in adjCells)
		self.assert_(m.cells[2][1] in adjCells)
		
	def testGetAdjacentUnblockedCells(self):
		m = Maze(3,3)
		adjCells = m.cells[0][0].getAllAdjacentUnblockedCells()
		self.assertEqual(0, len(adjCells))
		adjCells = m.cells[1][1].getAllAdjacentUnblockedCells()
		self.assertEqual(0, len(adjCells))
		m.cells[1][1].openPassageInDirection(east)
		m.cells[1][1].openPassageInDirection(north)
		adjCells = m.cells[1][1].getAllAdjacentUnblockedCells()
		self.assertEqual(2, len(adjCells))
		self.assert_(m.cells[0][1] in adjCells)
		self.assert_(m.cells[1][2] in adjCells)
		adjCells = m.cells[1][2].getAllAdjacentUnblockedCells()
		self.assertEqual(1, len(adjCells))
		self.assert_(m.cells[1][1] in adjCells)
		
	def testCellInPassageway(self):
		m = getFinishedTestMaze()
		self.assertEqual(True, m.cells[0][2].isInPassageway())
		self.assertEqual(True, m.cells[0][3].isInPassageway())
		self.assertEqual(True, m.cells[1][3].isInPassageway())
		self.assertEqual(True, m.cells[2][1].isInPassageway())
		self.assertEqual(True, m.cells[2][3].isInPassageway())
		self.assertEqual(False, m.cells[0][0].isInPassageway())
		self.assertEqual(False, m.cells[0][1].isInPassageway())
		self.assertEqual(False, m.cells[1][0].isInPassageway())
		self.assertEqual(False, m.cells[1][1].isInPassageway())
		self.assertEqual(False, m.cells[1][1].isInPassageway())
		self.assertEqual(False, m.cells[2][0].isInPassageway())
		self.assertEqual(False, m.cells[2][2].isInPassageway())
		
	def testGetExitDirectionForPassagewayCell(self):
		m = getFinishedTestMaze()
		self.assertEqual(m.cells[0][1], m.cells[0][2].getAdjacentPassagewayExitCell(m.cells[0][3]))
		self.assertEqual(m.cells[0][3], m.cells[0][2].getAdjacentPassagewayExitCell(m.cells[0][1]))
		self.assertEqual(m.cells[0][2], m.cells[0][3].getAdjacentPassagewayExitCell(m.cells[1][3]))
		self.assertEqual(m.cells[1][3], m.cells[0][3].getAdjacentPassagewayExitCell(m.cells[0][2]))
		self.assertEqual(m.cells[0][3], m.cells[1][3].getAdjacentPassagewayExitCell(m.cells[2][3]))
		self.assertEqual(m.cells[2][3], m.cells[1][3].getAdjacentPassagewayExitCell(m.cells[0][3]))
		self.assertEqual(m.cells[1][1], m.cells[2][1].getAdjacentPassagewayExitCell(m.cells[2][0]))
		self.assertEqual(m.cells[2][0], m.cells[2][1].getAdjacentPassagewayExitCell(m.cells[1][1]))
		

class HuntAndKillGeneratorTest(unittest.TestCase):
	def setUp(self):
		m = Maze(3,3)
		self.g = HuntAndKillGenerator(m)

	def testCreateGenerator(self):
		self.assertEqual(9, len(self.g.unvisited))
		self.assertEqual(0, len(self.g.visited))
	
	def testGenerateCompletesSuccessfully(self):
		self.g.generate()
		
	def testMoveCellFromUnvisitedToVisited(self):
		self.g.moveCellFromUnvisitedToVisited(3)
		self.assertEqual(8, len(self.g.unvisited))
		self.assertEqual(1, len(self.g.visited))
		self.assert_(3 in self.g.visited)
		self.assert_(3 not in self.g.unvisited)
   
	def testGetAllUnvisitedAdjacentCellsWithNewMaze(self):
		allUnvisitedCellOrdinals = self.g.getAllUnvisitedAdjacentCellOrdinals(self.g.maze.cells[1][1])
		validOrdinals = [1, 3, 5, 7]	# all adjacent cells are unvisited and are cells (aren't at the edge of a maze)
		[self.assert_(ord in allUnvisitedCellOrdinals) for ord in validOrdinals]

	def testGetAllUnvisitedAdjacentCellsNextToMazeEdge(self):
		allUnvisitedCellOrdinals = self.g.getAllUnvisitedAdjacentCellOrdinals(self.g.maze.cells[0][0])
		self.assert_(1 in allUnvisitedCellOrdinals)
		self.assert_(3 in allUnvisitedCellOrdinals)
		self.assertEqual(2, len(allUnvisitedCellOrdinals))

	def testGetAllUnvisitedAdjacentCellsInMazeWithVisitedCells(self):
		self.g.moveCellFromUnvisitedToVisited(1)
		self.g.moveCellFromUnvisitedToVisited(3)
		allUnvisitedCellOrdinals = self.g.getAllUnvisitedAdjacentCellOrdinals(self.g.maze.cells[1][1])
		self.assert_(5 in allUnvisitedCellOrdinals)
		self.assert_(7 in allUnvisitedCellOrdinals)
		self.assert_(1 not in allUnvisitedCellOrdinals)
		self.assert_(3 not in allUnvisitedCellOrdinals)
		self.assertEqual(2, len(allUnvisitedCellOrdinals))
		
	def testGetRandomValidAdjacentCell(self):
		g = getInProgressGeneratorWithVisitedCells()
		ac = g.getRandomValidAdjacentCell(g.maze.cells[1][1])
		self.assertEqual(None, ac)
		ac = g.getRandomValidAdjacentCell(g.maze.cells[1][3])
		self.assertEqual(None, ac)
		ac = g.getRandomValidAdjacentCell(g.maze.cells[2][2])
		self.assertEqual(None, ac)
		ac = g.getRandomValidAdjacentCell(g.maze.cells[0][1])
		self.assert_(ac in [g.maze.cells[0][0],g.maze.cells[0][2]])
		ac = g.getRandomValidAdjacentCell(g.maze.cells[1][0])
		self.assert_(ac in [g.maze.cells[0][0],g.maze.cells[2][0]])
		ac = g.getRandomValidAdjacentCell(g.maze.cells[2][1])
		self.assertEqual(g.maze.cells[2][0], ac)
		
	def testGetRandomVisitedCell(self):
		self.assertEqual(None, self.g.getRandomVisitedCell())	# at first no cells are visited
		self.g.moveCellFromUnvisitedToVisited(5)
		self.assertEqual(5, self.g.getRandomVisitedCell().ordinal())
		unvisitedCopy = self.g.unvisited[:]		# to iterate over while moving all to visited
		for i in unvisitedCopy: self.g.moveCellFromUnvisitedToVisited(i)
		self.assert_(self.g.getRandomVisitedCell().ordinal() in [0, 1, 2, 3, 4, 5, 6, 7, 8])
		

def getFinishedTestMaze():
	# maze looks like this:
	#  _________
	# |__  ___  |
	# |__  __|  | 
	# |____|____|
	m = Maze(3,4)
	m.cells[0][1].openPassageInDirection(east)
	m.cells[0][1].openPassageInDirection(west)
	m.cells[0][3].openPassageInDirection(west)
	m.cells[0][3].openPassageInDirection(south)
	for direction in directions:
		m.cells[1][1].openPassageInDirection(direction)
	m.cells[2][0].openPassageInDirection(east)
	m.cells[2][3].openPassageInDirection(north)
	m.cells[2][3].openPassageInDirection(west)
	return m

def getInProgressGeneratorWithVisitedCells():
	# the visited cells look like this:
	# UVUV
	# VVVV
	# UVVV
	#
	# This could match a maze like this, which could be created w/ code like that below
	# (but we don't need a maze when we're just testing visited/unvisited stuff in the generator)
	#  ___________
	# |__|  |_|  |
	# |___  __|  | 
	# |__|__|____|
	# m = Maze(3,4)
	# m.cells[0][3].openPassageInDirection(south)
	# for direction in directions:
	# 	m.cells[1][1].openPassageInDirection(direction)
	# m.cells[2][3].openPassageInDirection(north)
	# m.cells[2][3].openPassageInDirection(west)

	g = HuntAndKillGenerator(Maze(3,4))		# need width of four, so don't use default 3,3 maze/generator combo
	for ordinal in [1,3,4,5,6,7,9,10,11]: g.moveCellFromUnvisitedToVisited(ordinal)
	return g
		
		
if __name__ == '__main__':
	unittest.main()
