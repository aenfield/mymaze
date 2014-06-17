
import unittest
from mazeui import *


class MazeUITest(unittest.TestCase):
	def setUp(self):
		pass
	
	def testMazeUIConstructorWithDifferentParams(self):
		newMui = MazeUI(3,3,5,300,400)
		self.assertEqual(3, newMui.maze.width)
		self.assertEqual(3, newMui.maze.height)
		self.assertEqual(5, newMui.wallWidth)
		self.assertEqual(300, newMui.screenWidth)
		self.assertEqual(400, newMui.screenHeight)
		self.assertEqual(None, newMui.screen)
		newMuiAgain = MazeUI(3,3,screenWidth=300,wallWidth=5,screenHeight=400,screen='foo')
		self.assertEqual(3, newMuiAgain.maze.width)
		self.assertEqual(3, newMuiAgain.maze.height)
		self.assertEqual(5, newMuiAgain.wallWidth)
		self.assertEqual(300, newMuiAgain.screenWidth)
		self.assertEqual(400, newMuiAgain.screenHeight)
		self.assertEqual('foo', newMuiAgain.screen)
	
	def testMazeUIConstructorWithInnerWidth(self):
		mui = MazeUI(3,3,innerWidth=1)
		self.assertEqual(1, mui.innerWidth)
		mui = MazeUI(3,3,screenWidth=300,screenHeight=300)
		self.assertEqual(97, mui.innerWidth)	# innerWidth scales to fill screen size if not provided explicitly
	
	def testGetOriginForCellWithOnePixelWallsAndPassages(self):
		mui = MazeUI(3,3,wallWidth=1,innerWidth=1)
		self.assertEqual((0,0), mui.getOriginForCell(mui.maze.cells[0][0]))
		self.assertEqual((0,2), mui.getOriginForCell(mui.maze.cells[1][0]))
		self.assertEqual((2,0), mui.getOriginForCell(mui.maze.cells[0][1]))
		self.assertEqual((2,2), mui.getOriginForCell(mui.maze.cells[1][1]))
		self.assertEqual((4,4), mui.getOriginForCell(mui.maze.cells[2][2]))

	def testGetOriginForCellWithWiderWallsAndPassages(self):
		mui = MazeUI(3,3,wallWidth=2,innerWidth=3)
		self.assertEqual((0,0), mui.getOriginForCell(mui.maze.cells[0][0]))
		self.assertEqual((0,5), mui.getOriginForCell(mui.maze.cells[1][0]))
		self.assertEqual((5,0), mui.getOriginForCell(mui.maze.cells[0][1]))
		self.assertEqual((5,5), mui.getOriginForCell(mui.maze.cells[1][1]))
		self.assertEqual((10,10), mui.getOriginForCell(mui.maze.cells[2][2]))
	
	def testGetStartForWallsFromTheUpperLeftCell(self):
		mui = MazeUI(3,3,wallWidth=1,innerWidth=1)
		self.assertEqual((0,0), mui.getStartOfWallLine(mui.maze.cells[0][0], north))
		self.assertEqual((0,2), mui.getStartOfWallLine(mui.maze.cells[0][0], south))
		self.assertEqual((2,0), mui.getStartOfWallLine(mui.maze.cells[0][0], east))
		self.assertEqual((0,0), mui.getStartOfWallLine(mui.maze.cells[0][0], west))

	def testGetEndForWallsFromTheUpperLeftCell(self):
		mui = MazeUI(3,3,wallWidth=1,innerWidth=1)
		self.assertEqual((2,0), mui.getEndOfWallLine(mui.maze.cells[0][0], north))
		self.assertEqual((2,2), mui.getEndOfWallLine(mui.maze.cells[0][0], south))
		self.assertEqual((2,2), mui.getEndOfWallLine(mui.maze.cells[0][0], east))
		self.assertEqual((0,2), mui.getEndOfWallLine(mui.maze.cells[0][0], west))

	def testGetStartForWallsFromAMiddleCell(self):
		mui = MazeUI(3,3,wallWidth=1,innerWidth=1)
		self.assertEqual((2,2), mui.getStartOfWallLine(mui.maze.cells[1][1], north))
		self.assertEqual((2,4), mui.getStartOfWallLine(mui.maze.cells[1][1], south))
		self.assertEqual((4,2), mui.getStartOfWallLine(mui.maze.cells[1][1], east))
		self.assertEqual((2,2), mui.getStartOfWallLine(mui.maze.cells[1][1], west))

	def testGetEndForWallsFromAMiddleCell(self):
		mui = MazeUI(3,3,wallWidth=1,innerWidth=1)
		self.assertEqual((4,2), mui.getEndOfWallLine(mui.maze.cells[1][1], north))
		self.assertEqual((4,4), mui.getEndOfWallLine(mui.maze.cells[1][1], south))
		self.assertEqual((4,4), mui.getEndOfWallLine(mui.maze.cells[1][1], east))
		self.assertEqual((2,4), mui.getEndOfWallLine(mui.maze.cells[1][1], west))

	def testGetStartForWallsFromAMiddleCellWithWiderCellsAndPassages(self):
		mui = MazeUI(3,3,wallWidth=2,innerWidth=3)
		self.assertEqual((5,5), mui.getStartOfWallLine(mui.maze.cells[1][1], north))
		self.assertEqual((5,10), mui.getStartOfWallLine(mui.maze.cells[1][1], south))
		self.assertEqual((10,5), mui.getStartOfWallLine(mui.maze.cells[1][1], east))
		self.assertEqual((5,5), mui.getStartOfWallLine(mui.maze.cells[1][1], west))

	def testGetCenterForCell(self):
		mui = MazeUI(3,3,wallWidth=1,innerWidth=1)
		self.assertEqual((1,1), mui.getCenterForCell(mui.maze.cells[0][0]))
		self.assertEqual((3,3), mui.getCenterForCell(mui.maze.cells[1][1]))
		self.assertEqual((5,3), mui.getCenterForCell(mui.maze.cells[1][2]))
		mui = MazeUI(3,3,wallWidth=3,innerWidth=15)
		self.assertEqual((10,10), mui.getCenterForCell(mui.maze.cells[0][0]))
		self.assertEqual((28,10), mui.getCenterForCell(mui.maze.cells[0][1]))
		self.assertEqual((28,28), mui.getCenterForCell(mui.maze.cells[1][1]))
		
	def testGetCellOriginsWithOffset43Mazes(self):
		# see pixel calcs.xls for the math behind all of the offset cell origin expected results
		mui = MazeUI(4,3,wallWidth=1,screenWidth=800,screenHeight=600,offsetPixels=True)
		self.assertEqual((1,1), mui.getOriginForCell(mui.maze.cells[0][0]))
		self.assertEqual((1,200), mui.getOriginForCell(mui.maze.cells[1][0]))
		self.assertEqual((200,1), mui.getOriginForCell(mui.maze.cells[0][1]))
		self.assertEqual((200,200), mui.getOriginForCell(mui.maze.cells[1][1]))
		self.assertEqual((399,399), mui.getOriginForCell(mui.maze.cells[2][2]))
		mui = MazeUI(4,3,wallWidth=2,screenWidth=800,screenHeight=600,offsetPixels=True)
		self.assertEqual((1,0), mui.getOriginForCell(mui.maze.cells[0][0]))
		self.assertEqual((1,199), mui.getOriginForCell(mui.maze.cells[1][0]))
		self.assertEqual((200,0), mui.getOriginForCell(mui.maze.cells[0][1]))
		self.assertEqual((200,199), mui.getOriginForCell(mui.maze.cells[1][1]))
		self.assertEqual((399,398), mui.getOriginForCell(mui.maze.cells[2][2]))

	# I could use the following to test more of the offset math, if I udpated the expected
	# results using pixel calcs.xls, but I'll hold off unless I see issues in practice, since
	# the test above passes
	# def testGetCellOriginsWithOffsetNon43Mazes(self):
	# 	mui = MazeUI(5,4,wallWidth=2,screenWidth=800,screenHeight=600,offsetPixels=True)
	# 	self.assertEqual((0,0), mui.getOriginForCell(mui.maze.cells[0][0]))
	# 	self.assertEqual((0,2), mui.getOriginForCell(mui.maze.cells[1][0]))
	# 	self.assertEqual((2,0), mui.getOriginForCell(mui.maze.cells[0][1]))
	# 	self.assertEqual((2,2), mui.getOriginForCell(mui.maze.cells[1][1]))
	# 	self.assertEqual((4,4), mui.getOriginForCell(mui.maze.cells[2][2]))
	# 	mui = MazeUI(5,4,wallWidth=2,screenWidth=1200,screenHeight=600,offsetPixels=True)
	# 	self.assertEqual((0,0), mui.getOriginForCell(mui.maze.cells[0][0]))
	# 	self.assertEqual((0,5), mui.getOriginForCell(mui.maze.cells[1][0]))
	# 	self.assertEqual((5,0), mui.getOriginForCell(mui.maze.cells[0][1]))
	# 	self.assertEqual((5,5), mui.getOriginForCell(mui.maze.cells[1][1]))
	# 	self.assertEqual((10,10), mui.getOriginForCell(mui.maze.cells[2][2]))
	# 	mui = MazeUI(6,5,wallWidth=2,screenWidth=1200,screenHeight=600,offsetPixels=True)
	# 	self.assertEqual((0,0), mui.getOriginForCell(mui.maze.cells[0][0]))
	# 	self.assertEqual((0,5), mui.getOriginForCell(mui.maze.cells[1][0]))
	# 	self.assertEqual((5,0), mui.getOriginForCell(mui.maze.cells[0][1]))
	# 	self.assertEqual((5,5), mui.getOriginForCell(mui.maze.cells[1][1]))
	# 	self.assertEqual((10,10), mui.getOriginForCell(mui.maze.cells[2][2]))
	# 	mui = MazeUI(7,6,wallWidth=2,screenWidth=1200,screenHeight=600,offsetPixels=True)
	# 	self.assertEqual((0,0), mui.getOriginForCell(mui.maze.cells[0][0]))
	# 	self.assertEqual((0,5), mui.getOriginForCell(mui.maze.cells[1][0]))
	# 	self.assertEqual((5,0), mui.getOriginForCell(mui.maze.cells[0][1]))
	# 	self.assertEqual((5,5), mui.getOriginForCell(mui.maze.cells[1][1]))
	# 	self.assertEqual((10,10), mui.getOriginForCell(mui.maze.cells[2][2]))
	# 	
	# def testGetCellOriginsWithOffsetOLPCSimilarScreenDimensions(self):
	# 	mui = MazeUI(8,6,wallWidth=2,screenWidth=1200,screenHeight=650,offsetPixels=True)
	# 	self.assertEqual((0,0), mui.getOriginForCell(mui.maze.cells[0][0]))
	# 	self.assertEqual((0,5), mui.getOriginForCell(mui.maze.cells[1][0]))
	# 	self.assertEqual((5,0), mui.getOriginForCell(mui.maze.cells[0][1]))
	# 	self.assertEqual((5,5), mui.getOriginForCell(mui.maze.cells[1][1]))
	# 	self.assertEqual((10,10), mui.getOriginForCell(mui.maze.cells[2][2]))
		
		
	def testGetMazeDimensionsOfNextMazes(self):
		# for now, we're simple and only worry about 4:3 dimensions - 
		# so we add a column each time and row the first three out of every four times
		self.assertEqual((5,4), MazeUI(4,3).getDimensionsOfNextMaze())
		self.assertEqual((6,5), MazeUI(5,4).getDimensionsOfNextMaze())
		self.assertEqual((7,6), MazeUI(6,5).getDimensionsOfNextMaze())
		self.assertEqual((8,6), MazeUI(7,6).getDimensionsOfNextMaze())
		self.assertEqual((9,7), MazeUI(8,6).getDimensionsOfNextMaze())
		self.assertEqual((10,8), MazeUI(9,7).getDimensionsOfNextMaze())
		self.assertEqual((11,9), MazeUI(10,8).getDimensionsOfNextMaze())
		self.assertEqual((12,9), MazeUI(11,9).getDimensionsOfNextMaze())
		self.assertEqual((13,10), MazeUI(12,9).getDimensionsOfNextMaze())
		

	# TODO need to update these when I add width to walls 
	# def testGetEndForWallsFromAMiddleCellWithWiderCellsAndPassages(self):
		# self.assertEqual((4,2), getEndOfWallLine(mui.maze.cells[1][1], north, 2, 3))
		# self.assertEqual((4,4), getEndOfWallLine(mui.maze.cells[1][1], south, 2, 3))
		# self.assertEqual((4,4), getEndOfWallLine(mui.maze.cells[1][1], east, 2, 3))
		# self.assertEqual((2,4), getEndOfWallLine(mui.maze.cells[1][1], west, 2, 3))
		
	# TODO I could in theory actually test that draw walls sets the correct pixels using get_at (or whatever that method(s) called)
	#def testDrawWall(self):
	
	# TODO I could also in theory test that the current/visited circles are drawn where I want them to be drawn

	
	
if __name__ == '__main__':
	unittest.main()