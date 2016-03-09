import numpy as np
import cv2

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('/home/youngdp/workspace/haarcascade_frontalface_alt.xml')
kernel = np.ones((21,21),'uint8')
while(True):
	print x, y
	cv2.imshow('frame',frame)
    ret, frame = cap.read()
    faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(20,20))

	cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()