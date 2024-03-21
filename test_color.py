import cv2
import os
import numpy as np
from ansi.colour.rgb import rgb256

def get_terminal_color(pixel):
	if pixel[0] < 50 and pixel[1] < 50 and pixel[2] < 50:
		return 'black'
	pixel = tuple(pixel)
	return rgb256(pixel[0], pixel[1], pixel[2])

def resize_with_ratio(width, height, target_width = 0, target_height = 0):

	if target_width:
		ratio = target_width / float(width)
		new_height = int(height * ratio)
		return (target_width, new_height)
	if target_height:
		ratio = target_height / float(height)
		new_width = int(width * ratio)
		return (new_width, target_height)
	return (int(width), int(height))

def resize_image(image, width, height, columns, rows):
	x, y = width, height
	while x >= columns or y >= rows:
		x -= 1
		y -= 1
	if x == columns - 1:
		new_width, new_height = resize_with_ratio(width, height, target_width=x)
	else:
		new_width, new_height = resize_with_ratio(width, height, target_height=y)
	return (cv2.resize(image, (new_width, new_height)), new_width, new_height)

def get_four_lines(image, lineInd, lineSize):
	res = []
	for i in range(4):
		try:
			res.append(image[lineInd + i])
		except Exception:
			res.append([(0, 0, 0) for i in range(lineSize)])
	return res

def get_height_points(four_lines, colInd):
	res = []
	for j in range(2):
		for i in range(4):
			try:
				res.append(four_lines[i][colInd + j])
			except Exception:
				res.append((0, 0, 0))

	return res

def get_height_points_char(height_points):
	res = []
	val = 10495
	for i in range(len(height_points)):
		color = get_terminal_color(height_points[i])
		if color == 'black':
			val -= (2**i)
		else:
			res.append(color)
	if len(res) == 0:
		return chr(val)
	return max(set(res), key = res.count) + chr(val)

def print_points(image, width, height):
	y = 0
	while y < height:
		four_lines = get_four_lines(image, y, height)
		x = 0
		while x < width:
			height_points = get_height_points(four_lines, x)
			print(get_height_points_char(height_points),end="")
			x += 2
		print()
		y += 3

def get_terminal_size():
	rows, columns = os.popen('stty size', 'r').read().split()
	return int(rows), int(columns)

def simplify_colors(image):

	image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

	ranges = [
		((0, 50, 50), (10, 255, 255)),      # Rouge
		((20, 50, 50), (40, 255, 255)),     # Jaune
		((100, 50, 50), (130, 255, 255)),   # Bleu
		((40, 50, 50), (80, 255, 255)),     # Vert
		((10, 100, 100), (25, 255, 255)),   # Orange
		((140, 50, 50), (160, 255, 255)),   # Violet
		((0, 0, 0), (0, 50, 50)),        # Noir
		((0, 0, 220), (180, 30, 255))       # Blanc
	]

	colors = [
		(0, 0, 255),    # Rouge
		(0, 255, 255),  # Jaune
		(120, 255, 255),# Bleu
		(60, 255, 255), # Vert
		(20, 100, 255), # Orange
		(140, 255, 255),# Violet
		(0, 0, 0),      # Noir
		(0, 0, 255)     # Blanc
	]

	# Initialiser une image vide pour stocker l'image simplifiée
	simplified_image = np.zeros_like(image)

	# Mapper chaque pixel à la couleur la plus proche dans la liste des couleurs prédéfinies
	for i in range(len(ranges)):
		mask = cv2.inRange(image_hsv, ranges[i][0], ranges[i][1])
		simplified_image[mask > 0] = colors[i]

	return simplified_image

def main():
	image_path = "monkey.jpg"
	image = cv2.imread(image_path)

	new_height, new_width = get_terminal_size()
	new_height -= 1
	new_height *= 3
	new_width *= 2


	height, width, channels = image.shape

	resized_image, width, height = resize_image(image, width, height, new_width, new_height)
	color_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
	# color_image = simplify_colors(resized_image)
	# blackAndWhiteImage = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
	# image_simplified = cv2.cvtColor(resized_image, cv2.COLOR)
	# print(image_simplified	)

	print_points(color_image, width, height)

if __name__ == "__main__":
	main()

