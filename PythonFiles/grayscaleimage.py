import cv2

original_image = cv2.imread("image3.jpg")

grayscale_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY) 

cv2.imshow("grayscale_image", grayscale_image)
cv2.waitKey(0)

cv2.imwrite("saved_gray.jpg", grayscale_image) # saving grayscale image
