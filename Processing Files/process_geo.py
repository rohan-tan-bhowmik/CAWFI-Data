import cv2

bgr_img = cv2.imread('in.png')  ###CHANGE DIRECTORY TO INPUT GEOLOGICAL COLOR IMAGE***
hsv_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)[:,:,0]
cv2.imwrite('out.png', hsv_img) ###CHANGE DIRECTORY TO OUTPUT GEOLOGICAL MONOCHROME IMAGE***