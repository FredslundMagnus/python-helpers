import cv2
import numpy as np
import struct

outputVideo = cv2.VideoWriter()
outputVideo.open("foo.avi", -1, 25, (640, 480), True)

frame = np.zeros((480, 640, 3), dtype=np.uint8)
outputVideo.write(frame)
outputVideo.release()

inputVideo = cv2.VideoCapture("foo.avi")
fourcc = int(inputVideo.get(cv2.CAP_PROP_FOURCC))

print("FOURCC is '%s'" % struct.pack("<I", fourcc), fourcc)
while, if, return, for, else, raise, pass, break, try, except, yield, continue, assert, import, as
# sdfg while, if, return, for, else, raise, pass, break, try, except, yield, continue, assert, import, as
"while, if, return, for, else, raise, pass, break, try, except, yield, continue, assert, import, as"
'while, if, return, for, else, raise, pass, break, try, except, yield, continue, assert, import, as'
'''while, if, return, for, else, raise, pass, break, try, except, yield, continue, assert, import, as'''
"""while, if, return, for, else, raise, pass, break, try, except, yield, continue, assert, import, as"""
