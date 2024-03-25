import cv2
import os
import sys
from ansi.colour.rgb import rgb256
import threading


def get_terminal_color(pixel):
	if pixel[0] < 50 and pixel[1] < 50 and pixel[2] < 50:
		return 'black'
	# pixel = tuple(pixel)
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

def get_four_lines(image, lineInd):
	res = []
	for i in range(4):
		try:
			res.append(image[lineInd + i])
		except Exception:
			break
	return res

pow_list = [1, 2, 4, 8, 16, 32, 64, 128]

def get_height_points(four_lines, colInd):
	val = 10240
	for j in range(2):
		for i in range(4):
			try:
				if four_lines[i][colInd + j] > 127:
					val += pow_list[(j * 4) + i]
			except Exception:
				break
	return chr(val)

def print_points(image, width, height):
	y = 0
	content = ""
	while y < height:
		four_lines = get_four_lines(image, y)
		x = 0
		while x < width:
			content += get_height_points(four_lines, x)
			x += 2
		content += '\n'
		y += 4
	sys.stdout.write(content + (y >> 2) * "\033[F")

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
		blackAndWhiteImage = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

		print_points(blackAndWhiteImage, width, height)

	cap.release()
	show_cursor()

def main():
	video_path = "Top 5 Shrek.mp4"
	process_video(video_path)

if __name__ == "__main__":
	main()
