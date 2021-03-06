import numpy as np
import cv2
import sys

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
def show_realtime_detection(img, overlay, overlayMode = True) :
    
    font = cv2.FONT_ITALIC
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
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
                
        if overlayMode : 
            overlayResized = cv2.resize(overlay, dsize=(w, h), interpolation=cv2.INTER_AREA)
            y1, y2 = y, y + overlayResized.shape[0]
            x1, x2 = x, x + overlayResized.shape[1]

            overlayAlpha = overlayResized[:, :, 3] / 255.0
            imgAlpha = 1.0 - overlayAlpha
            for c in range(0, 3):
                img[y1:y2, x1:x2, c] = (overlayAlpha * overlayResized[:, :, c] +
                                        imgAlpha * img[y1:y2, x1:x2, c])    

    return img        
        
        

    
if __name__ == '__main__' :
    if len(sys.argv) < 2 :
        print('Please specify overlay image path')
        exit()
    cap = cv2.VideoCapture(0)
    overlayMode = True
    cap.set(3,640) # set Width
    cap.set(4,480) # set Height

    overlay = cv2.imread(sys.argv[1], -1)
    while True :
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        cv2.imshow('video', show_realtime_detection(img, overlay, overlayMode))
        k = cv2.waitKey(1) & 0xff
        if k == 27: # press 'ESC' to 
            break
        elif k == 97 or k == 65:
            overlayMode = not overlayMode
            print('Overlay Mode = ', overlayMode)

    cap.release()
    cv2.destroyAllWindows()
