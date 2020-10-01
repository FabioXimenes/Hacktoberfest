import cv2

image = cv2.imread("image3.jpg") # read image

cv2.imshow("imagem", image) # show image
cv2.waitKey(0) 

cv2.imwrite("saved.jpg", image) # save image
