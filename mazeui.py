
import pygame
import random
import time		# for sleep
from pygame.locals import *
from sys import exit
from maze import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MAZE_WIDTH = 4
MAZE_HEIGHT = 3
KEY_REPEAT_DELAY = 300		# ms, amount of time to repeat held down key events
AUTO_MOVE_DELAY = 0.1		# sec (for time.sleep) and to delay between automatic moves

BACKGROUND_COLOR = (0, 0, 0)
CURRENT_COLOR = (0, 255, 0)
VISITED_COLOR = (0, 96, 0)
FINISH_COLOR = (0, 0, 96)

def main():
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
	pygame.key.set_repeat(KEY_REPEAT_DELAY, KEY_REPEAT_DELAY)		# send repeated KEYDOWN events if a key is held down

	lastCell = None
	mui, currentCell = createAndDrawNewMaze(MAZE_WIDTH, MAZE_HEIGHT, screen)

	while True:
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				nextCell = mui.moveToNewCellWithUserInput(currentCell, event.key)
				if nextCell:
					lastCell, currentCell = drawCellsAndReturnLastAndNowCurrentCells(mui, currentCell, nextCell)
			if event.type == QUIT:
				exit()
		
		mui, currentCell, lastCell = createNewMazeIfCurrentMazeSolved(mui, currentCell, lastCell)		
		
		while lastCell != None and currentCell.isInPassageway():
			# we can keep on moving, automatically
			time.sleep(AUTO_MOVE_DELAY)	# pause for just a bit so we don't move too fast
			nextCell = currentCell.getAdjacentPassagewayExitCell(lastCell)
			lastCell, currentCell = drawCellsAndReturnLastAndNowCurrentCells(mui, currentCell, nextCell)
			mui, currentCell, lastCell = createNewMazeIfCurrentMazeSolved(mui, currentCell, lastCell)		
			

def drawCellsAndReturnLastAndNowCurrentCells(mui, currentCell, newCurrentCell):
	"""Draws the new current cell as current and the old current cell as visited, and then returns the same references as last cell and the now-current cell."""
	mui.drawCurrentCellAndVisitLastCell(currentCell, newCurrentCell)
	pygame.display.update()

	lastCell, currentCell = currentCell, newCurrentCell	# obviously could be combined, but this explicit code at least says what I'm trying to mean (somewhat)
	return lastCell, currentCell

def createAndDrawNewMaze(mazeWidth, mazeHeight, screen):
	"""Creates a new MazeUI instance, generates a maze, and then draws it. Returns both the MazeUI instance and the current/start cell."""
	mui = MazeUI(mazeWidth, mazeHeight, screenWidth=SCREEN_WIDTH, screenHeight=SCREEN_HEIGHT, screen=screen, offsetPixels=True)
	HuntAndKillGenerator(mui.maze).generate()
	mui.screen.fill(BACKGROUND_COLOR)
	mui.drawMaze()

	# start off in the upper-left corner
	currentCell = mui.maze.cells[0][0]	
	mui.drawCurrentCell(currentCell)
	pygame.display.update()

	return mui, currentCell

def createNewMazeIfCurrentMazeSolved(mui, currentCell, lastCell):
	"""Create and return a new maze if the current cell is the same as the finish cell. If not, just return what was passed in (to make it easier to call this w/o conditional code)."""
	if currentCell == mui.maze.finishCell:
		# woohoo - finished the maze. pause a few secs and then start a new one with one more row and col
		time.sleep(2)
		newWidth, newHeight = mui.getDimensionsOfNextMaze()
		lastCell = None
		mui, currentCell = createAndDrawNewMaze(newWidth, newHeight, mui.screen)
	return mui, currentCell, lastCell


class MazeUI(object):
	def __init__(self, mazeWidth, mazeHeight, wallWidth=2, screenWidth=SCREEN_WIDTH, screenHeight=SCREEN_HEIGHT, screen=None, innerWidth=None, offsetPixels=False):
		self.maze = Maze(mazeHeight, mazeWidth)
		self.wallWidth = wallWidth
		self.screenWidth = screenWidth
		self.screenHeight = screenHeight
		self.screen = screen
		if innerWidth != None:
			self.innerWidth = innerWidth
		else:
			# scale cell innerWidth to fill the screen, using the smaller of the screen height or width so it fits
			if screenHeight <= screenWidth:
				self.innerWidth = (self.screenHeight - ((self.maze.height + 1) * self.wallWidth)) / self.maze.height 
			else:
				self.innerWidth = (self.screenWidth - ((self.maze.width + 1) * self.wallWidth)) / self.maze.width	
		self.offsetPixels = offsetPixels
		if self.offsetPixels:
			actualScreenWidthUsed = ((self.maze.width + 1) * self.wallWidth) + (self.maze.width * self.innerWidth)
			actualScreenHeightUsed = ((self.maze.height + 1) * self.wallWidth) + (self.maze.height * self.innerWidth)
			self.widthPixelOffset = (self.screenWidth - actualScreenWidthUsed) / 2
			self.heightPixelOffset = (self.screenHeight - actualScreenHeightUsed) / 2
		else:
			self.widthPixelOffset = 0
			self.heightPixelOffset = 0
	
	def drawMaze(self):
		for cell in flatten(self.maze.cells):
			for direction in directions:
				if (cell.walls[direction] in blocked): self.drawWall(cell, direction)
		self.drawCircle(FINISH_COLOR, self.maze.finishCell)
	
	def moveToNewCellWithUserInput(self, currentCell, key):
		"""Move from the current cell to a specified new cell, using a K_UP, etc 'key'. Return the new current cell, or None if the cell doesn't change (because a non-directional key was pressed or because the direction was blocked, for example)."""
		nextCell = None		
		directionalKeys = [K_UP, K_RIGHT, K_DOWN, K_LEFT]
		if key in directionalKeys:
			direction = {K_UP:    north,
						 K_RIGHT: east,
						 K_DOWN:  south,
						 K_LEFT:  west}[key]
			if currentCell.walls[direction] not in blocked:
				nextCell = currentCell.getAdjacentCell(direction)

		return nextCell
			
	def moveToRandomNewCellAndDraw(self, currentCell):
		"""Just for fun, randomly visit cells in the maze, including drawing. Return the new current cell."""
		# If called from the main loop like the following, the maze'll be visited randomly
		# currentCell = moveToRandomNewCell(currentCell)
		# pygame.display.update()
		nextCell = random.choice(currentCell.getAllAdjacentUnblockedCells())
		self.drawCurrentCellAndVisitLastCell(currentCell, nextCell)
		return nextCell
				
	def drawCurrentCellAndVisitLastCell(self, currentCell, nextCell):
		"""Draw 'nextCell' as the current cell and 'currentCell' as visited"""
		self.drawCircle(CURRENT_COLOR, nextCell)
		self.drawCircle(VISITED_COLOR, currentCell)
	
	def drawCurrentCell(self, currentCell):
		self.drawCircle(CURRENT_COLOR, currentCell)

	def drawWall(self, cell, direction):
		"""Draw a wall, for the provided 'cell', in the provided 'direction'. Doesn't check to see if there's actually a wall in that direction (you should do that before calling this method)."""
		origin = self.getOriginForCell(cell)
		start = self.getStartOfWallLine(cell, direction)
		end = self.getEndOfWallLine(cell, direction)
		pygame.draw.line(self.screen, (128,128,128), start, end, self.wallWidth)

	def drawCircle(self, color, cell):
		cellCenter = self.getCenterForCell(cell)
		radius = self.innerWidth / 3
		pygame.draw.circle(self.screen, color, cellCenter, radius)	

	def getStartOfWallLine(self, cell, direction):
		x, y = self.getOriginForCell(cell)
		cellDiff = self.wallWidth + self.innerWidth
		start = {north: (x, y),
				 south: (x, y + cellDiff),
				 east:  (x + cellDiff, y),
				 west:  (x, y)}[direction]
		return start

	def getEndOfWallLine(self, cell, direction):
		x, y = self.getOriginForCell(cell)
		cellDiff = self.wallWidth + self.innerWidth
		end =   {north: (x + cellDiff, y),
				 south: (x + cellDiff, y + cellDiff),
				 east:  (x + cellDiff, y + cellDiff),
				 west:  (x, y + cellDiff)}[direction]
		return end

	def getOriginForCell(self, cell):
		# the pixel offsets are set to 0 if we don't specify that we want offsetting when we create the maze UI
		x = self.widthPixelOffset + (cell.col * (self.wallWidth + self.innerWidth))
		y = self.heightPixelOffset + (cell.row * (self.wallWidth + self.innerWidth))
		return (x, y)

	def getCenterForCell(self, cell):
		cellOrigin = self.getOriginForCell(cell)
		centerOffset = ((2 * self.wallWidth) + self.innerWidth) / 2
		return (cellOrigin[0] + centerOffset, cellOrigin[1] + centerOffset)
	
	def getDimensionsOfNextMaze(self):
		# for now, we're simple and only worry about 4:3 dimensions - so we add a column each time and row the first three out of every four times
		# there's a way to automate this for any aspect ratio, but I won't worry about that if I don't need it
		# for 4:3, then, we add a new row EXCEPT when (width % 4) = 3
		newWidth = self.maze.width + 1
		if (self.maze.width % 4) != 3:
			newHeight = self.maze.height + 1
		else: 
			newHeight = self.maze.height
		
		return (newWidth, newHeight)
	
# could be a non-maze UI utility function
def flatten(list):
	"""Flattens the passed list - which can have nested lists, like you might get with maze.cells - into a single list."""
	return sum(list, [])
	

if __name__ == '__main__':
    main()