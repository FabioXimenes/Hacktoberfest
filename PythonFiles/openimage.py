#  Abrir uma imagem colorida, visualizar e salvar.

import cv2

imagem = cv2.imread("image3.jpg") # le imagem

cv2.imshow("imagem", imagem) # mostra
cv2.waitKey(0) 

cv2.imwrite("saved.jpg", imagem) #salva
