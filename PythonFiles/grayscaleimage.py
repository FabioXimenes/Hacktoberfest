# Abrir uma imagem colorida, transformar em níveis de cinza, visualizar e salvar imagem gerada.

import cv2

image = cv2.imread("image3.jpg")

grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

cv2.imshow("grayscale_image", grayscale_image)
cv2.waitKey(0)

cv2.imwrite("saved_gray.jpg", grayscale_image)
