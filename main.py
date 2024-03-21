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
	return cv2.resize(image, (new_width, new_height))

def get_terminal_size():
	rows, columns = os.popen('stty size', 'r').read().split()
	return int(rows), int(columns)

def custom_image_processing(image, dimensions):
	image = resize_image(image)
	print('dimensions :', dimensions)

def process_video(video_path):

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

		if not ret:
			break

		custom_image_processing(frame, dimensions)

	cap.release()

def main():
	video_path = "votre_video.mp4"
	process_video(video_path)

if __name__ == "__main__":
	main()
