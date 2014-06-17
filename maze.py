
import random
import logging
if __name__ == '__main__': 
	#logging.basicConfig(level=logging.INFO)
	logging.basicConfig(level=logging.DEBUG)	# turns on verbose logging and stepped output


# enumerated type for directions with respect to cells
north, east, south, west = range(4)	
directions = [north, south, east, west]

# things that the edge of a cell can have
wall, permanentwall, passage = range(3)
blocked = [wall, permanentwall]


class Maze(object):
	def __init__(self, height, width):
		self.height = height
		self.width = width
		
		# list comprehension, creates new rows with 'width' cells, once for each 'height'
		self.cells = [[Cell(row, col, self) for col in range(width)] for row in range(height)]
		
		# set maze edges to permanentwall
		# TODO now that cells know their position, can this move to init or somewhere else?
		for rownum in [0, height - 1]:
			for colnum in [0, width - 1]:
				if rownum == 0:
					self.cells[rownum][colnum].walls[north] = permanentwall
				if rownum == self.height - 1:
					self.cells[rownum][colnum].walls[south] = permanentwall 
				if colnum == 0:
					self.cells[rownum][colnum].walls[west]  = permanentwall 
				if colnum == self.width - 1:
					self.cells[rownum][colnum].walls[east]  = permanentwall
					
		# by default, start is upper left and finish is lower right
		self.startCell = self.cells[0][0]
		self.finishCell = self.cells[self.height - 1][self.width - 1]
		

	def cellPositionToOrdinal(self, row, col):
		"""returns a single number that identifies the cell"""
		return (row * self.width) + col
		
	def ordinalToCellPosition(self, ordinal):
		"""returns a (row, col) cell position given an ordinal"""
		row = ordinal / self.width
		col = ordinal % self.width
		return (row, col)
	
	def ordinalToCell(self, ordinal):
		row, col = self.ordinalToCellPosition(ordinal)
		return self.cells[row][col]
		
	def isCellPositionInMaze(self, row, col):
		if (row < 0) or (row >= self.height) or (col < 0) or (col >= self.width):
			return False
		else:
			return True

	@classmethod
	def reverseOf(self, direction):
		return {east:  west,
    			west:  east,
			    north: south,
			    south: north}[direction]

	# return an ASCII art version of the maze
	def __str__(self):	
		s  = ' ' + '_'*((self.width * 2) - 1) + ' \n'			# header row, just '_'
		for row in self.cells:
			s += '|' + ''.join([str(s) for s in row]) + '\n'	# let each cell draw itself, and create a string from the resulting list

		return s
		

class Cell(object):
	def __init__(self, row, col, maze=None, northWall=wall, eastWall=wall, southWall=wall, westWall=wall):
		self.row = row
		self.col = col
		self.maze = maze
		self.walls = [northWall, eastWall, southWall, westWall]
		
	def openPassageInDirection(self, direction):
		self.walls[direction] = passage
		self.getAdjacentCell(direction).walls[Maze.reverseOf(direction)] = passage
		# TODO check for impassible edges instead of assuming it's ok to set a passage no matter what		
		
	def openPassageToCell(self, destinationCell):
		"""opens a passage to the specified cell, which must be adjacent"""
		self.openPassageInDirection(self.getDirectionOfAdjacentCell(destinationCell))
		# TODO check for non-adjacent destination cell
		
	def getDirectionOfAdjacentCell(self, adjacentCell):
		rowDiff, colDiff = adjacentCell.row - self.row, adjacentCell.col - self.col
		return {(-1, 0): north,
				( 0, 1): east,
				( 1, 0): south,
				( 0,-1): west}[(rowDiff, colDiff)]	# it would be nice if I could reuse this dict, in reverse, so I don't duplicate it in getAdjacentCell
	
	def getAdjacentCell(self, direction):
		rowChange, colChange = {north: (-1, 0),
								east:  ( 0, 1),
								south: ( 1, 0),
								west:  ( 0,-1)}[direction]
		newRow, newCol = self.row + rowChange, self.col + colChange

		# ('-1' indexes backwards, so we can't just catch IndexError and return None)
		if self.maze.isCellPositionInMaze(newRow, newCol):
			return self.maze.cells[newRow][newCol]
		else:
			return None
		# TODO since this relies on self.maze, check for it and raise appropriate exception if there's no maze
	
	def getAllAdjacentCells(self):
		return [self.getAdjacentCell(direction) for direction in directions if self.getAdjacentCell(direction) != None]

	def getAllAdjacentUnblockedCells(self):
		return [self.getAdjacentCell(direction) for direction in directions if self.walls[direction] not in blocked]
	
	def ordinal(self):
		return self.maze.cellPositionToOrdinal(self.row, self.col)

	def isInPassageway(self):
		"""Returns if this cell is in a 'passageway,' which means it has only an entrance and exit - i.e., there's no choice a user can make in this cell, and we could possibly keep on moving out the side from which the user didn't enter."""
		if len([wall for wall in self.walls if wall not in blocked]) == 2:
			return True
		else:
			return False
			
	def getAdjacentPassagewayExitCell(self, entryCell):
		"""Assuming this cell is a passageway (has only one entrance and one exit), returns the cell that's adjacent to this cell's exit. 'entryCell' is the cell from which this cell was entered."""
		for direction in directions:
			if (self.walls[direction] not in blocked) and (self.getAdjacentCell(direction) != entryCell):
				return self.getAdjacentCell(direction)

	# return an ASCII art version - only the right (east) and bottom (south) walls matter,
	# the other walls are handled by other cells (above and to the left)
	def __str__(self):
		# Following two lines don't work with Python 2.4, so we replace with multi-line if/else code
		# s  = '_' if (self.walls[south] in blocked) else ' '
		# s += '|' if (self.walls[east]  in blocked) else '_'
		if self.walls[south] in blocked:
			s = '_'
		else:
			s = ' '
		
		if self.walls[east] in blocked:
			s += '|'
		else:
			s += '_'
			
		return s
		
	def __repr__(self):
		return '<Cell at [%s][%s]>' % (self.row, self.col)


# Uses a variant of the hunt-and-kill algorith, per http://www.aarg.net/~minam/dungeon_design.html:
# 1. Start with a rectangular grid, x units wide and y units tall. Mark each cell in the grid 
#    unvisited.
# 2. Pick a random cell in the grid and mark it visited. This is the current cell.
# 3. From the current cell, pick a random direction (north, south, east, or west). If (1) there is 
#    no cell adjacent to the current cell in that direction, or (2) if the adjacent cell in that 
#    direction has been visited, then that direction is invalid, and you must pick a different 
#    random direction. If all directions are invalid, pick a different random visited cell in 
#    the grid and start this step over again.
# 4. Let's call the cell in the chosen direction C. Create a corridor between the current cell 
#    and C, and then make C the current cell. Mark C visited.
# 5. Repeat steps 3 and 4 until all cells in the grid have been visited.
#
class HuntAndKillGenerator(object):
	def __init__(self, maze):
		self.maze = maze
		self.unvisited = range(self.maze.width * self.maze.height)
		self.visited = []
				
	def generate(self):		
		currentCellOrdinal = random.choice(self.unvisited)
		self.moveCellFromUnvisitedToVisited(currentCellOrdinal)
		currentCell = self.maze.ordinalToCell(currentCellOrdinal)
		
		while len(self.unvisited) > 0:
			logging.debug('Processing cell [%s][%s] with ordinal %s.' % (currentCell.row, currentCell.col, currentCell.ordinal()))
			logging.debug('Visited: %s, Unvisited: %s' % (self.visited, self.unvisited))
			validAdjacentCell = None
			while validAdjacentCell == None:
				validAdjacentCell = self.getRandomValidAdjacentCell(currentCell)
				
				logging.debug('\n%s' % self.maze)
				if logging.getLogger().getEffectiveLevel() <= logging.DEBUG: raw_input('Press return to continue ')
				logging.debug('\n%s' % ('-'*40))
				
				if validAdjacentCell == None: 	# we're stopped here, so pick another visited cell to start again
					currentCell = self.getRandomVisitedCell()
					logging.debug('No valid adjacent cells... choosing a different visited cell to try next: %s.' % (currentCell.ordinal()))

			currentCell.openPassageToCell(validAdjacentCell)
			
			self.moveCellFromUnvisitedToVisited(validAdjacentCell.ordinal())
			currentCell = validAdjacentCell
		
		logging.info('Finished.\n%s' % (self.maze))


	def moveCellFromUnvisitedToVisited(self, cellOrdinal):
		self.unvisited.remove(cellOrdinal)
		self.visited.append(cellOrdinal)
	
	def getAllUnvisitedAdjacentCellOrdinals(self, startCell):
		"""returns a list of ordinals for each adjacent cell that's not been visited, or [] if all adjacent cells have been visited."""
		allAdjacentCells = startCell.getAllAdjacentCells()
		return [cell.ordinal() for cell in allAdjacentCells if cell.ordinal() in self.unvisited]

	def getRandomValidAdjacentCell(self, currentCell):
		possibleValidAdjacentCellOrdinals = self.getAllUnvisitedAdjacentCellOrdinals(currentCell)
		logging.debug('Valid adjacent cell ordinals are: %s' % (possibleValidAdjacentCellOrdinals))
		
		if possibleValidAdjacentCellOrdinals != []:
			return self.maze.ordinalToCell(random.choice(possibleValidAdjacentCellOrdinals))
		else:
			return None
			
	def getRandomVisitedCell(self):
		if self.visited != []:
			return self.maze.ordinalToCell(random.choice(self.visited))
		else:
			return None
			
			
			
if __name__ == '__main__':
	height = int(raw_input('Enter height of maze: '))
	width = int(raw_input('Enter width of maze: '))
	m = Maze(height, width)
	g = HuntAndKillGenerator(m)
	g.generate()
