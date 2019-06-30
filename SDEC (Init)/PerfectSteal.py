import cv2
import numpy as np
import predict
from time import sleep

def Reset():
    global seq, pred
    
    seq = ''
    pred = ''

def RefreshScreen():
    img[:] = (255,255,255)
    cv2.putText(img, f'{seq}', (32,64), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(img, f'{pred}', (32,128), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow('Real Time Steal Predictor', img)

img = np.zeros((500, 500, 3),np.uint8)
Reset()
elements = ['a','s','d','g','f','s','e']

predict.PredictSingle(['sss'], 'RoberAsk_2-2', '10samples')

# 
while True:
    k = cv2.waitKey(20)

    RefreshScreen()

    # 
    for l in elements:
        if k == ord(l):
            seq += l
            sleep(.1)

    # 
    if k == 8:
        Reset()

    if k == 13:
        pred = "Predicting..."
        p = predict.PredictSingle([seq], 'RoberAsk_2-2', '10samples')
        pred = "Steal" if p == 1 else "Don't Steal"
        
    # 
    if k == 27:
        break

cv2.destroyAllWindows()