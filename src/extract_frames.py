# Extracts the individual image frames from a video file
# Tested for (mp4 -> jpg) and (mov -> jpg)

import argparse
import cv2
import sys


# Simply prints to stdout without a newline
def flushed_std_out(s):
  sys.stdout.write(s)
  sys.stdout.flush()


# Convert hh:mm:ss to number of milliseconds
def convert_timestring_to_msec(string):
	number_of_values = len(string.split(':'))
	msec = 0
	for i, val in enumerate(string.split(':')):
		if number_of_values - i == 1:
			msec += int(val) * 1000
		elif number_of_values - i == 2:
			msec += int(val) * 60000
		elif number_of_values - i == 3:
			msec += int(val) * 3600000
	return msec


def extract_frames(args):
	# Open video file and print stats
	cap = cv2.VideoCapture(args.input_file)
	frame_count = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
	if args.verbose:
		print 'Filename: ' + args.input_file
		print 'Open success?: ' + str(cap.isOpened())
		print 'Frame width: %d' % cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
		print 'Frame height: %d' % cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
		print 'FPS: ' + str(cap.get(cv2.cv.CV_CAP_PROP_FPS))
		print 'Frame count: %d' % frame_count

	# Get length in msec of movie, then reset
	cap.set(cv2.cv.CV_CAP_PROP_POS_AVI_RATIO, 1)
	len_in_msec = cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
	cap.set(cv2.cv.CV_CAP_PROP_POS_AVI_RATIO, 0)

	# Compute frames to capture
	start_msec = convert_timestring_to_msec(args.start) if args.start else 0
	end_msec = convert_timestring_to_msec(args.end) if args.end else len_in_msec
	start_frame = int(start_msec / len_in_msec * frame_count)
	end_frame = int(end_msec / len_in_msec * frame_count)
	if args.verbose:
		print 'Extracting frames %d to %d.' % (start_frame, end_frame)

	# Extract
	cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, start_frame)
	for frame_num in xrange(start_frame, end_frame + 1):
		success, image = cap.read()
		if not success or cv2.waitKey(10) == 27: # Exit if Escape key is hit
			break
		cv2.imwrite(args.output_file_root + '%d.jpg' % frame_num, image)
		if args.verbose and frame_num % 100 == 0:
			flushed_std_out('.')
	if args.verbose:
		print # newline
		print 'Done!'


if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description='Extract frames from a video file.')
	parser.add_argument('input_file', type=str,
		help='Video to extract frames from.')
	parser.add_argument('output_file_root', type=str,
		help='Output file root. E.g. "images/video_name" will result in files ' +
				 'like "images/video_name34.jpg".')
	parser.add_argument('--start', type=str,
		help='Start time in hh:mm:ss format. Defaults to beginning of file. ' +
		'ssssss or mmm:ss etc formats also work.')
	parser.add_argument('--end', type=str,
		help='Start time in hh:mm:ss format. Defaults to beginning of file. ' +
		'ssssss or mmm:ss etc formats also work.')
	parser.add_argument('--verbose', action='store_true',
		help='Update on progress.')
	args = parser.parse_args()
	extract_frames(args)