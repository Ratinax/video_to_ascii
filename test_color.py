import cv2
import os
import numpy as np
from ansi.colour.rgb import rgb256

def get_terminal_color(pixel):
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
		if color == '"[38;5;232m"':
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

	print_points(color_image, width, height)

if __name__ == "__main__":
	main()
