class player:
	def __init__(self, xPos = 0, yPos = 0, advanceIncrement = 1, color = (0, 255, 0)): #can set advance increment so that advance can be called on player to easily increase position
		self.x = xPos
		self.y = yPos
		self.increment = advanceIncrement
		self.inAir = False
		self.color = color
		self.jumpHeight = 0
		player.goingUp = True
	def setPos(self, xPos, yPos): #set the new position
		self.x = xPos
		self.y = yPos
		