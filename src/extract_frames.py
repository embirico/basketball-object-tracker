# Extracts the individual image frames from a video file
# Tested for mp4 -> jpg

import argparse
import cv2
import sys


# Simply prints to stdout without a newline
def flushedStdOut(s):
    sys.stdout.write(s)
    sys.stdout.flush()


def main(args):
	vidcap = cv2.VideoCapture(args.input_file)

	count = 0
	while True:
		success, image = vidcap.read()
		if not success or cv2.waitKey(10) == 27: # Exit if Escape key is hit
			break
		cv2.imwrite(args.output_file_root + '%d.jpg' % count, image)
		if args.verbose and count % 100 == 0:
			flushedStdOut('.')
		count += 1
	print # newline


if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description='Extract frames from a video file.')
	parser.add_argument('input_file', type=str,
		help='Video to extract frames from.')
	parser.add_argument('output_file_root', type=str,
		help='Output file root. E.g. "images/video_name" will result in files ' +
				 'like "images/video_name34.jpg".')
	parser.add_argument('--verbose', action='store_true',
		help='Update on progress.')
	args = parser.parse_args()
	main(args)