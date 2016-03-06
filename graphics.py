#graphics
import pygame
import random

pygame.init()
pygame.display.init()
size = (1020, 1020)
screen = pygame.display.set_mode(size)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
screen.fill(black)

def create_map(num_lines):
	hole_size = 10
	map = []
	for i in range(1000):
		nested_map = []
		for j in range(num_lines):
			nested_map.append(1)
		map.append(nested_map)

	"""#make holes
	for i in range(100):
		width = random.randint(5, 25)
		depth = random.randint(5, 15)
		index1 = random.randint(0, 1000)
		index2 = random.randint(0, 50)
		for j in range(width):
			for k in range(depth):
				if index1 + depth < 1000 and index2 + width < num_lines:
					map[index1 + depth][index2 + width] = 0
		map"""

	make_zero_width = 0
	make_zero_depth = 0
	for i in range(1000):
		for j in range(num_lines):
			if random.randint(0, 400) == 0 and make_zero_width <= 0:
				make_zero_width = random.randint(2, 30)
			if random.randint(0, 1000) == 0 and make_zero_depth <= 0:
				make_zero_depth = random.randint(2, 8)
			if make_zero_width > 0 or make_zero_depth > 0:
				map[i][j] = 0
			make_zero_width -= 1
		make_zero_depth -= 1
	return map

	
def update(coordinate1, coordinate2, coordinate3, coordinate4):
	done = False
	index = 1
	while not done:
		pygame.display.update()
		draw_grid(coordinate1, map1, index, screen, num_lines, (0, 125, 125))
		draw_grid(coordinate2, map2, index, screen, num_lines, (0, 125, 125))
		draw_grid(coordinate3, map3, index, screen, num_lines, (125, 0, 125))
		draw_grid(coordinate4, map4, index, screen, num_lines, (125, 0, 125))
		pygame.time.wait(20)
		index += 1
		print index
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit(); sys.exit();

def draw_grid(coordinates, map, index, screen, num_lines, input_color):
	copy = index
	for i in range(num_lines):
		for j in range(num_lines):
			color = (0, 0, 0)
			if (map[j + index][i] == 1):
				color = input_color
			count = i * (num_lines) + j
			pygame.draw.polygon(screen, color, coordinates[-count], 0)

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
			if side == 'left' or side == 'right':
				coordinates.append([p1, p2, p3, p4])
				rand_color = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))
				pygame.draw.polygon(screen, rand_color, [p1, p2, p3, p4], 0)
			elif side == 'bottom' or side == 'top':
				coordinates.append([reflect_point(p1), reflect_point(p2), reflect_point(p3), reflect_point(p4)])
				rand_color = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))
				pygame.draw.polygon(screen, rand_color, [reflect_point(p1), reflect_point(p2), reflect_point(p3), reflect_point(p4)], 0)
	return coordinates

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
	print p1, " ", p2
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


width = 1020
height = 1020
num_lines = 60
depth = 400
left_coordinates = create_coordinates('left', width, height, num_lines, depth)
right_coordinates = create_coordinates('right', width, height, num_lines, depth)
bottom_coordinates = create_coordinates('bottom', width, height, num_lines, depth)
top_coordinates = create_coordinates('top', width, height, num_lines, depth)
map1 = create_map(num_lines)
map2 = create_map(num_lines)
map3 = create_map(num_lines)
map4 = create_map(num_lines)
update(left_coordinates, right_coordinates, bottom_coordinates, top_coordinates)