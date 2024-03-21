import cv2
import os

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

def resize_image(image, width, height, rows, columns):
	x, y = width, height
	while x > columns or y > rows:
		x -= 1
		y -= 1
	if x == columns:
		new_width, new_height = resize_with_ratio(width, height, target_width=x)
	else:
		new_width, new_height = resize_with_ratio(width, height, target_height=y)
	return (cv2.resize(image, (new_width, new_height)), new_width, new_height)

def get_three_lines(image, lineInd, lineSize):
	res = []
	for i in range(3):
		try:
			res.append(image[lineInd + i])
		except Exception:
			res.append([(0, 0, 0) for i in range(lineSize)])
	return res

def get_six_points(three_lines, colInd):
	res = []
	for j in range(2):
		for i in range(3):
			try:
				res.append(three_lines[i][colInd + j])
			except Exception:
				res.append((0, 0, 0))

	return res

def getIsBlack(point):
	if isinstance(point, tuple):
		return point == (0, 0, 0)

	if (int(point) > 127):
		return False
	return True

def get_six_points_char(six_points):
	val = 10240
	for i in range(6):
		val += (2**i) * (getIsBlack(six_points[i]) == 0)
	return chr(val)

def print_points(image, width, height):
	y = 0
	while y < height:
		three_lines = get_three_lines(image, y, height)
		x = 0
		while x < width:
			six_points = get_six_points(three_lines, x)
			print(get_six_points_char(six_points),end="")
			x += 2
		print()
		y += 3

def get_terminal_size():
	rows, columns = os.popen('stty size', 'r').read().split()
	return int(rows), int(columns)

def main():
	image_path = "monkey.jpg"
	image = cv2.imread(image_path)

	new_width, new_height = get_terminal_size()
	new_width -= 1
	new_width *= 3
	new_height *= 2

	height, width, channels = image.shape

	resized_image, width, height = resize_image(image, width, height, new_width, new_height)

	blackAndWhiteImage = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

	print_points(blackAndWhiteImage, width, height)

if __name__ == "__main__":
	main()
