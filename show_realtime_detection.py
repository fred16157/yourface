import numpy as np
import cv2

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
pepe = cv2.imread('./images/pepeOverlay.png', -1)
box = cv2.imread('./images/1000.png', -1)
cap = cv2.VideoCapture(0)
font = cv2.FONT_ITALIC
cap.set(3,640) # set Width
cap.set(4,480) # set Height
faceMode = False
eyeMode = False
pepeMode = False
boxMode = False

while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cv2.putText(img, "FaceMode - " + str(faceMode) + " EyeMode - " + str(eyeMode) + " PepeMode - " + str(pepeMode) + " BoxMode - " + str(boxMode), (20, 20), font, 0.5, (0, 0, 255), 2)

    if faceMode :
        faces = faceCascade.detectMultiScale(
            gray,     
            scaleFactor=1.2,
            minNeighbors=5,     
            minSize=(10, 10)
        )
        for (x,y,w,h) in faces:
            print('face detected')
            
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            cv2.putText(img, "Detected Face", (x-5, y-5), font, 0.5, (255,255,0),2)
            

            if pepeMode : 
                pepeResized = cv2.resize(pepe, dsize=(w, h), interpolation=cv2.INTER_AREA)
                y1, y2 = y, y + pepeResized.shape[0]
                x1, x2 = x, x + pepeResized.shape[1]
                pepeAlpha = pepeResized[:, :, 3] / 255.0
                imgAlpha = 1.0 - pepeAlpha

                for c in range(0, 3):
                    img[y1:y2, x1:x2, c] = (pepeAlpha * pepeResized[:, :, c] +
                                            imgAlpha * img[y1:y2, x1:x2, c])
            elif boxMode :
                boxResized = cv2.resize(box, dsize=(w, h), interpolation=cv2.INTER_AREA)
                y1, y2 = y, y + boxResized.shape[0]
                x1, x2 = x, x + boxResized.shape[1]
                boxAlpha = boxResized[:, :, 3] / 255.0
                imgAlpha = 1.0 - boxAlpha

                for c in range(0, 3):
                    img[y1:y2, x1:x2, c] = (boxAlpha * boxResized[:, :, c] +
                                            imgAlpha * img[y1:y2, x1:x2, c])                

            if eyeMode:
                bbGray = gray[y:y+h, x:x+w]
                bbColor = img[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(bbGray, 
                    scaleFactor= 1.5,
                    minNeighbors=10,
                    minSize=(2, 2),
                )
                for (ex,ey,ew,eh) in eyes:
                    cv2.rectangle(bbColor, (ex, ey), (ex+ew, ey+eh), (0,255,0), 2)
        
    cv2.imshow('video',img)
    k = cv2.waitKey(1) & 0xff
    if k == 27: # press 'ESC' to quit
        break
    elif k == 97 or k == 65:
        faceMode = not faceMode
        print('toggled FaceMode:', faceMode)
    elif k == 98 or k == 66:
        eyeMode = not eyeMode
        print('toggled EyeMode:', eyeMode)
    elif k == 99 or k == 67:
        pepeMode = not pepeMode
        print('toggled PepeMode:', pepeMode)
    elif k == 100 or k == 68:
        boxMode = not boxMode
        print('toggled BoxMode:', boxMode)

cap.release()
cv2.destroyAllWindows()