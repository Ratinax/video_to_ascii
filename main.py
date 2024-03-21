import cv2
import os
import sys
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
	nbLines = 0
	while y < height:
		four_lines = get_four_lines(image, y, height)
		x = 0
		while x < width:
			height_points = get_height_points(four_lines, x)
			print(get_height_points_char(height_points),end="")
			x += 2
		print()
		nbLines += 1
		y += 3
	return nbLines

def get_terminal_size():
	rows, columns = os.popen('stty size', 'r').read().split()
	return int(rows), int(columns)


def hide_cursor():
	sys.stdout.write('\033[?25l')
	sys.stdout.flush()
def show_cursor():
	sys.stdout.write('\033[?25h')
	sys.stdout.flush()

def process_video(video_path):
	# Open file
	cap = cv2.VideoCapture(video_path)
	hide_cursor()

	# Read first image to have size
	ret, frame = cap.read()
	if not ret:
		print("Error while reading video.")
		return

	# Get size
	new_height, new_width = get_terminal_size()
	new_height -= 1



	# While on each image
	while True:
		# Read next image
		ret, frame = cap.read()
		if not ret:
			break
		height, width, channels = frame.shape
		resized_image, width, height = resize_image(frame, width, height, new_width, new_height)
		color_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)


		nbLines = print_points(color_image, width, height)
		for i in range(nbLines):
			sys.stdout.write("\033[F")

	cap.release()
	show_cursor()

def main():
	video_path = "Top 5 Shrek.mp4"
	process_video(video_path)

if __name__ == "__main__":
	main()
