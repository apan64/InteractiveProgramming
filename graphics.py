#graphics
import pygame, random, sys, time, cv2, threading
import numpy as np
from plane import plane
from player import player

pygame.init()
pygame.display.init()
size = (1020, 1020)
screen = pygame.display.set_mode(size)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
middle = 250
screen.fill(black)
faceCoordinates = []

def create_map(num_lines):
	hole_size = 10
	map = []
	for i in range(10000):
		nested_map = []
		for j in range(num_lines):
			nested_map.append(1)
		map.append(nested_map)

	make_zero_width = 0
	make_zero_depth = 0
	for i in range(10000):
		for j in range(num_lines):
			if random.randint(0, 400) == 0 and make_zero_width <= 0:
				make_zero_width = random.randint(5, 30)
			if random.randint(0, 1000) == 0 and make_zero_depth <= 0:
				make_zero_depth = random.randint(5, 8)
			if make_zero_width > 0 or make_zero_depth > 0:
				map[i][j] = 0
			make_zero_width -= 1
		make_zero_depth -= 1
	return map

def read_frame(run):
	cap = cv2.VideoCapture(0)
	face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')
	kernel = np.ones((21,21),'uint8')
	while(True):
		et, frame = cap.read()
		ret, frame = cap.read()
		faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minSize=(20,20))
		print faces
		for (x,y,w,h) in faces:
			if(x == None or y == None):
				faceCoordinates.append((middle, middle))
			else:
				faceCoordinates.append((x, y))
		if(not run.running):
			break
def move_x(x):
	if int(x) - middle < -10:
		return 10
	elif int(x) - middle > 10:
		return -10
	return 0
def check_jump(value):
	if (middle - value) > 40:
		return True
	return False
def update(coordinate1, coordinate2, coordinate3, coordinate4, map1, map2, map3, map4, player, num_lines, fThread, run):
	done = False
	index = 1
	maps = [map1, map2, map3, map4]
	myfont = pygame.font.SysFont("monospace", 20)
	score = 0
	max_score = 0
	while not done:
		pygame.display.update()
		try:
			(x, y) = faceCoordinates.pop()
		except IndexError:
			(x, y) = (middle, middle)
		keys = pygame.key.get_pressed()
		player.x += move_x(x)
		if(player.x > 100):
				player.x -= 10
		else:
			player.x = 900
			maps = [maps[2], maps[3], maps[1], maps[0]]

		if(player.x < 920):
			player.x += 10
		else:
			player.x = 120
			maps = [maps[3], maps[2], maps[0], maps[1]]

		if(keys[pygame.K_LEFT] != 0):
			if(player.x > 100):
				player.x -= 10
			else:
				player.x = 900
				maps = [maps[2], maps[3], maps[1], maps[0]]
		elif(keys[pygame.K_RIGHT] != 0):
			if(player.x < 920):
				player.x += 10
			else:
				player.x = 120
				maps = [maps[3], maps[2], maps[0], maps[1]]
		if((keys[pygame.K_UP] != 0 or check_jump(y)) and not player.inAir):
			player.goingUp = True
			player.inAir = True
		elif(player.inAir):
			if(player.jumpHeight <= 0 and not player.goingUp):
				player.jumpHeight = 0
				player.inAir = False
			elif(player.goingUp and player.jumpHeight < 80):
				player.jumpHeight += 10
			elif(player.goingUp and player.jumpHeight >= 80):
				player.goingUp = False
			else:
				player.jumpHeight -= 10
		locs = round_player_loc(player.x, width, num_lines)
		if collision(maps[3], locs, index, player.inAir):
			score = 0
		draw_grid(coordinate1, maps[0], index, screen, num_lines, False, locs, False, player.inAir) #left
		draw_grid(coordinate2, maps[1], index, screen, num_lines, True, locs, False, player.inAir) #right
		draw_grid(coordinate3, maps[2], index, screen, num_lines, True, locs, False, player.inAir) #top
		draw_grid(coordinate4, maps[3], index, screen, num_lines, False, locs, True, player.inAir) #bottom
		
		score += 1
		if score > max_score:
			max_score = score
		show_score(score, max_score, myfont, width, height)
		draw_player(player, screen)
		pygame.time.wait(8)
		index += 1
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run.running = False
				pygame.quit(); sys.exit();

def show_score(score, max_score, myfont, width, height):
	pygame.draw.rect(screen, (0, 0, 0), (width / 2 - 100, height / 2 - 100, 200, 200), 0)
	label = myfont.render(str(score), 1, (255, 255, 255))
	label2 = myfont.render("Max score: " + str(max_score), 1, (255, 255, 255))
	screen.blit(label2, (width / 2 - 90, height / 2 - 50))
	screen.blit(label, (width / 2 - 50, height / 2))

def round_player_loc(x, width, num_lines):
	new_x = 1.0 * (width - x) / width * num_lines
	values_to_check = []
	fix = 0
	if new_x < num_lines / 3:
		fix = -1
	elif new_x > 2 * num_lines / 3:
		fix = 1
	for i in range(-2, 2):
		values_to_check.append([int(new_x) + i + fix, 2])
	return values_to_check

def draw_player(player, screen):
	pygame.draw.circle(screen, player.color, [player.x, player.y - player.jumpHeight], 30)

def draw_grid(coordinates, mapC, index, screen, num_lines, reverse, locs, bottom, in_air):
	for i in range(num_lines):
		for j in range(num_lines):
			color = (0, 0, 0)
			if not reverse:
				if (mapC.map[j + index][i] == 1):
					color = mapC.color
				count = i * (num_lines) + j
				if bottom and not in_air:
					for loc in locs:				
							if loc[0] == i and j == loc[1]:
								color = (255, 0, 0)
				pygame.draw.polygon(screen, color, coordinates[-count], 0)
			else:
				if (mapC.map[j + index][-i] == 1):
					color = mapC.color
				count = i * (num_lines) + j
				pygame.draw.polygon(screen, color, coordinates[-count], 0)

def collision(mapC, locs, index, in_air):
	if in_air:
		return False
	for loc in locs:
		x = loc[1] + index
		y = loc[0]
		if mapC.map[x][y] == 0:
			return True
	return False


def create_coordinates(side, width, height, num_lines, depth):
	y_loc = height / 2
	interval = width / num_lines
	horizon_line = [depth, 'vertical']
	x = 0
	if side == 'right' or side == 'top':
		x = width
		horizon_line = [width - depth, 'vertical']


	lines = []
	for i in range(num_lines + 1):
		lines.append(find_slope_intercept([x, interval * i], [width / 2, y_loc]))
		red = (255, 0, 0)
		#pygame.draw.line(screen, red, [x, interval * i], [width / 2, y_loc], 2)


	point = find_intersection(horizon_line, lines[0])

	cross_line = find_slope_intercept(point, [x, height])
	#pygame.draw.line(screen, green, point, [x, height], 2)

	vert_lines = []
	for i in range(num_lines + 1):
		intersection = find_intersection(cross_line, lines[i])
		vert_lines.append(create_vertical_line(intersection))

	coordinates = []
	for i in range(len(lines) - 1):
		for j in range(len(vert_lines) - 1):
			p1 = find_intersection(lines[i], vert_lines[j])
			p2 = find_intersection(lines[i + 1], vert_lines[j])
			p3 = find_intersection(lines[i + 1], vert_lines[j + 1])
			p4 = find_intersection(lines[i], vert_lines[j + 1])
			if side == 'left':
				coordinates.append([p1, p2, p3, p4])
				rand_color = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))
				pygame.draw.polygon(screen, rand_color, [p1, p2, p3, p4], 0)
			elif side == 'right':
				coordinates.append([p1, p2, p3, p4])
				rand_color = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))
				pygame.draw.polygon(screen, rand_color, [p1, p2, p3, p4], 0)
			elif side == 'bottom':
				coordinates.append([reflect_point(p1), reflect_point(p2), reflect_point(p3), reflect_point(p4)])
				rand_color = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))
				pygame.draw.polygon(screen, rand_color, [reflect_point(p1), reflect_point(p2), reflect_point(p3), reflect_point(p4)], 0)
			elif side == 'top':
				coordinates.append([reflect_point(p1), reflect_point(p2), reflect_point(p3), reflect_point(p4)])
				rand_color = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))
				pygame.draw.polygon(screen, rand_color, [reflect_point(p1), reflect_point(p2), reflect_point(p3), reflect_point(p4)], 0)
	return coordinates

def flip_horizontal(width, height, p):
	return [width - p[0], p[1]]

def flip_vertical(width, height, p):
	return [p[0], height - p[1]]


def reflect_point(p):
	return [p[1], p[0]]

def find_intersection(l1, l2):
	l1_b0 = l1[0]
	l1_b1 = l1[1]
	l2_b0 = l2[0]
	l2_b1 = l2[1]
	if l1_b1 == 'vertical':
		return [l1_b0, int(l2_b0 + 1.0 * l2_b1 * l1_b0)]
	elif l2_b1 == 'vertical':
		return [l2_b0, int(l1_b0 + 1.0 * l1_b1 * l2_b0)]
	else:
		x = 1.0 * (l1_b0 - l2_b0) / (l2_b1 - l1_b1)
		y = l1_b0 + l1_b1 * x
		return [int(x), int(y)]

def find_slope_intercept(p1, p2):
	# print p1, " ", p2
	p1_x = p1[0]
	p1_y = p1[1]
	p2_x = p2[0]
	p2_y = p2[1]
	run = p2_x - p1_x
	rise = p2_y - p1_y
	if run == 0:
		return [p1_x, 'vertical']
	slope = 1.0 * rise / run
	return [1.0 * p1_y - slope * p1_x, slope]

def create_vertical_line(p):
	p_x = p[0]
	p_y = p[1]
	return [p_x, 'vertical']

def create_horizontal_line(p):
	p_x = p[0]
	p_y = p[1]
	return [p_y, 0]

class running:
	def __init__(self):
		self.running = False

if __name__ == '__main__':
	width = 1020
	height = 1020
	num_lines = 30
	depth = 400
	left_coordinates = create_coordinates('left', width, height, num_lines, depth)
	right_coordinates = create_coordinates('right', width, height, num_lines, depth)
	top_coordinates = create_coordinates('top', width, height, num_lines, depth)
	bottom_coordinates = create_coordinates('bottom', width, height, num_lines, depth)
	play = player(510, 925)
	map1 = plane(1, play, (0, 125, 125))
	map2 = plane(2, play, (0, 125, 125))
	map3 = plane(3, play, (125, 0, 125))
	map4 = plane(4, play, (125, 0, 125))
	map1.populate(10000, num_lines, 6)
	map2.populate(10000, num_lines, 6)
	map3.populate(10000, num_lines, 6)
	map4.populate(10000, num_lines, 6)
	r = running()
	try:
		faceThread = threading.Thread(target = read_frame, name = 'face', args = (r,))
		gameThread = threading.Thread(target = update, name = 'game', args = (left_coordinates, right_coordinates, bottom_coordinates, top_coordinates, map1, map2, map3, map4, play, num_lines, faceThread, r))
		gameThread.start()
		r.running = True
		faceThread.start()
		gameThread.join()
		faceThread.join()
	except IndexError:
		while True:
			pygame.display.update()
			pygame.draw.rect(screen, (0, 0, 0), (width / 2 - 100, height / 2 - 100, 200, 200), 0)
			label = pygame.font.SysFont("comicsansms", 50).render('You made it', 1, (0, 255, 0))
			label2 = pygame.font.SysFont("comicsansms", 50).render('to the end!', 1, (0, 255, 0))
			screen.blit(label, (width / 2 - 100, height / 2 - 50))
			screen.blit(label2, (width / 2 - 95, height / 2 - 20))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					r.running = False
					pygame.quit(); sys.exit();