# coding:utf-8

import cv2
cap=cv2.VideoCapture(0)
while True:
    ret,frame=cap.read()
    if ret:
        cv2.imshow("capture",frame)
        #按键 q退出
        if cv2.waitKey(1)& 0xFF==ord('q'):
            file_name="eric.jpeg"
            cv2.imwrite(file_name,frame)
            break
    else:
        break

cap.release()
cap.destroyAllWindows()



