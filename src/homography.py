import image_object as IO
import json


if __name__ == '__main__':
	with open('manual_points.json', 'r') as f:
		data = json.load(f)
	print data["5993"]
