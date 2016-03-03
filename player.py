class player:
	def __init__(self, xPos = 0, yPos = 0, advanceIncrement = 1): #can set advance increment so that advance can be called on player to easily increase position
		self.x = xPos
		self.y = yPos
		self.increment = advanceIncrement
	def setPos(self, xPos, yPos): #set the new position
		self.x = xPos
		self.y = yPos
	def advance(self):
		self.y += self.increment
		