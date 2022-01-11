import cv2
import numpy as np
import time
from datetime import datetime

count = 0
background = 0
recording_filename = ''
window_name = 'Image'
radius = 20
color = (0, 0, 255)
thickness = -1
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
center_coordinates = (int(wCam - 35), int(radius + 28))

# time.sleep(3)


for i in range(60):
	return_val, background = cap.read()
	if return_val == False :
		continue

background = np.flip(background, axis = 1)
is_recording = False
while (cap.isOpened()):
	return_val, img = cap.read()
	if not return_val :
		break
	count = count + 1
	img = np.flip(img, axis = 1)

	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	lower_red = np.array([100, 40, 40])	
	upper_red = np.array([100, 255, 255])
	mask1 = cv2.inRange(hsv, lower_red, upper_red)

	lower_red = np.array([155, 40, 40])
	upper_red = np.array([180, 255, 255])
	mask2 = cv2.inRange(hsv, lower_red, upper_red)

	mask1 = mask1 + mask2

	mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations = 2)
	mask1 = cv2.dilate(mask1, np.ones((3, 3), np.uint8), iterations = 1)
	mask2 = cv2.bitwise_not(mask1)

	res1 = cv2.bitwise_and(background, background, mask = mask1)
	res2 = cv2.bitwise_and(img, img, mask = mask2)
	img = cv2.addWeighted(res1, 1, res2, 1, 0)
	if is_recording:
		out.write(img)
	cv2.imshow(window_name, img)
	k = cv2.waitKey(10)
	if k == 27:
		print('ESC pressed')
		break
	elif k == 191:
		print('F2 pressed\nCapturing Background')
		for i in range(60):
			return_val, background = cap.read()
			if return_val == False :
				continue
		background = np.flip(background, axis = 1)
		print('Background Captured')
	elif k == 115 and is_recording:
		print('R pressed')
		is_recording = False
		out.release()
		print('Recording Stopped')
	elif k == 114 and not is_recording:
		print('S pressed')
		is_recording = True
		recording_filename = "output" + str(datetime.now().isoformat().split(".")[0].replace(":","-")) + ".avi"
		fourcc = cv2.VideoWriter_fourcc(*'XVID')
		out = cv2.VideoWriter(recording_filename,fourcc,20.0, (wCam,hCam))
		print('Recording Started')
	
cap.release()
if is_recording:
	out.release()
	print('Recording Stopped')
cv2.destroyAllWindows()