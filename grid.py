#World
import pygame
import random

def main():

	pygame.init()
	pygame.display.init()
	size = (1200, 1000)
	screen = pygame.display.set_mode(size)
	red = (255, 0, 0)
	green = (0, 255, 0)
	blue = (0, 0, 255)
	black = (0, 0, 0)
	screen.fill(black)
	"""
	#horizontal
	height = 1000
	width = 1000
	num_lines = 10

	bottom_interval = width / num_lines
	left_interval = height / num_lines


	left_lines = []
	bottom_lines = []
	for i in range(num_lines):
		[b0, b1] = find_line([width / 2, 0], [i * left_interval, height])
		print "left", [b0, b1]
		left_lines.append([b0, b1])

	for i in range(num_lines):
		[b0, b1] = find_line([0, width / 2], [height, i * bottom_interval])
		print "bottom",[b0, b1]
		bottom_lines.append([b0, b1])

	horizon = 300
	left_horizon_Line = [horizon, 'vertical']
	bottom_horizon_line = [horizon, 'vertical']

	left_cross_line = find_intersection(left_lines[-1], left_horizon_Line)
	bottom_cross_line = find_intersection(bottom_lines[-1], bottom_horizon_line)
	print left_cross_line
	print bottom_cross_line

	#horizon_point1 = find_intersection(top_line, horizon_line)
	#horizon_point2 = find_intersection(top_line, horizon_line)
	#pygame.draw.line(screen, green, horizon_point, [horizon_x, 0])
	"""
	
	
	width = 1800
	height = 1000
	vanishing_point_x = 0
	vanishing_point_y = height / 2
	num_lines = 100
	y_interval = height / num_lines
	horizon_x = 400

	width2 = height / 2
	height2 = height
	vanishing_point_x2 = height2 / 2
	vanishing_point_y2 = 0
	num_lines2 = num_lines
	y_interval2 = height2 / num_lines2
	horizon_x = 200

	map = []
	for i in range(1000):
		nested_map = []
		for j in range(num_lines):
			nested_map.append(random.randint(0, 1))
		map.append(nested_map)

	map2 = []
	for i in range(1000):
		nested_map2 = []
		for j in range(num_lines):
			nested_map.append(random.randint(0, 1))
		map2.append(nested_map)

	lines = []
	for i in range(num_lines):
		#print [width, i * y_interval]
		[b0, b1] = find_line([0, height / 2], [width, i * y_interval])
		lines.append([b0, b1])


	top_line = lines[-1]
	horizon_line = [horizon_x, 'vertical']
	horizon_point = find_intersection(top_line, horizon_line)
	#pygame.draw.line(screen, green, horizon_point, [horizon_x, 0])

	cross_line = find_line(horizon_point, [width, 0])
	points = []
	for i in range(num_lines):
		points.append(find_intersection(lines[i], cross_line))

	for i in range(len(points)):
		#pygame.draw.circle(screen, green, points[i], 10, 1)
		pass

	#pygame.draw.line(screen, blue, horizon_point, [width, 0])
	for i in range(num_lines):
		pygame.draw.line(screen, red, [0, height2 / 2], [width2, i * (y_interval2)], 2)
		pass

	vert_lines = []
	for i in range(len(points)):
		vert_lines.append([points[i][0], 'vertical'])
		vert_point = find_intersection(top_line, vert_lines[i])
		#pygame.draw.line(screen, red, vert_point, [points[i][0], 0], 6)

	coordinates = []
	for i in range(len(lines) - 1):
		for j in range(len(vert_lines) - 1):
			p1 = find_intersection(lines[i], vert_lines[j])
			p2 = find_intersection(lines[i + 1], vert_lines[j])
			p3 = find_intersection(lines[i + 1], vert_lines[j + 1])
			p4 = find_intersection(lines[i], vert_lines[j + 1])
			coordinates.append([p1, p2, p3, p4])
			rand_color = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))
			pygame.draw.polygon(screen, rand_color, [p1, p2, p3, p4], 0)


	print len(coordinates)
	done = False
	index = 0
	
	while not done:
		draw_grid(coordinates, map, index, screen, num_lines)
		pygame.display.update()
		pygame.time.wait(1000)
		index += 1
		print index
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit(); sys.exit();


def draw_grid(coordinates, map, index, screen, num_lines):
	copy = index
	for i in range(num_lines - 1):
		for j in range(num_lines - 1):
			color = (0, 0, 0)
			if (map[j + index][i] == 1):
				color = (0, 125, 125)
			count = i * (num_lines - 1) + j
			pygame.draw.polygon(screen, color, coordinates[count], 0)


def find_polygon():
	pass

def find_intersection(l1, l2):
	l1_b0 = l1[0]
	l1_b1 = l1[1]
	l2_b0 = l2[0]
	l2_b1 = l2[1]

	#if one of the lines is vertical
	if (l1_b1 == 'vertical'):
		return [l1_b0, l2_b0 + l2_b1 * l1_b0]
	if (l2_b1 == 'vertical'):
		return [l2_b0, l1_b0 + l1_b1 * l2_b0]
	x = (l1_b0 - l2_b0) / (l2_b1 - l1_b1)
	y = l1_b0 + l1_b1 * x
	return [int(x), int(y)]

def find_line(p1, p2):
	p1_x = p1[0]
	p1_y = p1[1]
	p2_x = p2[0]
	p2_y = p2[1]
	if (p2_x - p1_x == 0):
		return [p2_x, 'vertical']
	b1 = -1.0 * (p2_y - p1_y) / (p2_x - p1_x)
	b0 = 1.0 * p1_y + b1 * p1_x
	return [b0, b1]
	

main()