import cv2
import os
import sys

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

	# print('resized to', new_width, new_height)
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
	nbLines = 0
	while y < height:
		three_lines = get_three_lines(image, y, height)
		x = 0
		while x < width:
			six_points = get_six_points(three_lines, x)
			print(get_six_points_char(six_points),end="")
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
		blackAndWhiteImage = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)


		nbLines = print_points(blackAndWhiteImage, width, height)
		for i in range(nbLines):
			sys.stdout.write("\033[F")

	cap.release()
	show_cursor()

def main():
	video_path = "Top 5 Shrek.mp4"
	process_video(video_path)

if __name__ == "__main__":
	main()
