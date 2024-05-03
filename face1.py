import cv2
import os

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
imgBackground = cv2.imread('Resources/background.png')
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = [cv2.imread(os.path.join(folderModePath, path)) for path in modePathList]

while True:
    success, img = cap.read()
    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[0]
    #cv2.imshow("webcam", img)
    cv2.imshow("Face Attendance", imgBackground)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif cv2.getWindowProperty("Face Attendance", cv2.WND_PROP_VISIBLE) < 1:  # quit window
        break

cap.release()
cv2.destroyAllWindows()
