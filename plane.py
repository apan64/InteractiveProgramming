class plane:
	import random
	def __init__(self, player, planeMap = []):
		self.planeNum = p #identify which plane this is
		self.player = p #the player
		self.map = planeMap #matrix of points for floor/holes
	# def advance(self, amount): #advances current y-position by an amount
	# 	self.pos[1] += amount
	# 	return self.pos
	# def shift(self, amount): #shifts current x-position by an amount
	# 	self.pos[0] += amount
		# return self.pos
	def populate(self, numRows, numCols): #randomly populate itself
		self.map = []
		for x in range(numRows):
			self.map.append([(1 if random.randint(1, 5) < 5 else 0) for i in range(numCols)]) #floors are weighted 4x more than holes
	def onFloor(self): #returns True if the current position is on an existing floor, false if it is on a hole
		return (self.map[int(self.player.x)][int(self.player.y)] == 1) #1 constitutes floor, 0 indicates hole
