from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
import cv2
import numpy as np
import predict

img = np.zeros((500, 500, 3),np.uint8)
seq = ''
pred = 'pred'
alphabet = []

# 
for letter in range(97,123):
    alphabet.append(chr(letter))
# 
while True:
    k = cv2.waitKey(20)

    img[:] = (255,255,255)
    cv2.putText(img, f'{seq}', (32,64), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(img, f'{pred}', (32,128), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow('Real Time Steal Predictor', img)

    # 
    for l in alphabet:
        if k == ord(l):
            seq += l

    # 
    if k == 8:
        seq = ''

    if k == 13:
        predict.PredictSingle([seq], 'RoberAsks', '50samples')
        print(f"PREDICT {seq}!")

    # 
    if k == 27:
        break

cv2.destroyAllWindows()