basketball-object-tracker
=========================

CS 231 Project Winter 2014

Project to perform single-view 3D reconstruction of basketball scenes
using commonly available TV footage of games.

Our main objective is to identify location of court relative to camera.

Source code is located in the `src` directory:

* To get an understanding of how the 4-point selection works, look at
  `image_object.py`, which calls most other files.
  (This script can be run without arguments.)
* The homography estimation is done in `homography.py`.
	(This script can be run without arguments.)
* Frame extraction is done in `extract_frames.py`.
	(This script requires arguments, which you can find by running with `-h`.)
