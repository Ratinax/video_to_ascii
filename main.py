import cv2
import os


def get_terminal_size():
	rows, columns = os.popen('stty size', 'r').read().split()
	return int(rows), int(columns)

def resize_with_ratio(width, height, target_width = 0, target_height = 0):

	if target_width:
		ratio = target_width / float(width)
		new_height = int(height * ratio)
		return (target_width, new_height)
	if target_height:
		ratio = target_height / float(height)
		new_width = int(width * ratio)
		return (new_width, target_height)
	return (width, height)

def resize_image(image, width, height, rows, columns):
	x, y = width, height
	while x > columns or y > rows:
		x -= 1
		y -= 1
	if x == columns:
		new_width, new_height = resize_with_ratio(width, height, target_height=y)
	else:
		new_width, new_height = resize_with_ratio(width, height, target_width=x)
	return cv2.resize(image, (new_width, new_height)), new_width, new_height

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


def process_video(video_path):
	rows, column = get_terminal_size()

	# Open file
	cap = cv2.VideoCapture(video_path)

	# Read first image to have size
	ret, frame = cap.read()
	if not ret:
		print("Erreur lors de la lecture de la vidéo.")
		return

	# Get size
	dimensions = (frame.shape[1], frame.shape[0])

	# While on each image
	while True:
		# Read next image
		ret, frame = cap.read()
		resized_image = resize_image(frame, dimensions[0], dimensions[1], rows, column)
		blackAndWhiteImage = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

		if not ret:
			break

		custom_image_processing(blackAndWhiteImage, dimensions)

	cap.release()

def main():
	video_path = "votre_video.mp4"
	process_video(video_path)

if __name__ == "__main__":
	main()
