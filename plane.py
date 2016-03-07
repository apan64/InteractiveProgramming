import random
class plane:
	def __init__(self, num, pl, color, planeMap = []):
		self.planeNum = num #identify which plane this is
		self.player = pl #the player
		self.map = planeMap #matrix of points for floor/holes
		self.color = color
	# def advance(self, amount): #advances current y-position by an amount
	# 	self.pos[1] += amount
	# 	return self.pos
	# def shift(self, amount): #shifts current x-position by an amount
	# 	self.pos[0] += amount
		# return self.pos
	def populate(self, numRows, numCols, size): #randomly populate itself
		self.map = []
		mapRef = []
		weight = 4
		for x in range(numRows/size):
			mapRef.append([(1 if random.randint(1, weight) < weight else 0) for i in range(numCols/size)]) #floors are weighted more than holes
		for row in mapRef:
			realRow = []
			for entry in row:
				for i in range(size):
					realRow.append(entry)
			for i in range(size):
				self.map.append(realRow)
		return self.map
	def onFloor(self): #returns True if the current position is on an existing floor, false if it is on a hole
		return (self.map[int(self.player.x)][int(self.player.y)] == 1) #1 constitutes floor, 0 indicates hole
