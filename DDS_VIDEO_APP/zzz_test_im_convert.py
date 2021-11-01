
from PySide6 import QtCore
from PySide6 import QtGui

import numpy as np
import cv2

def main():
    '''
    '''
    image_name = "C:\\Users\\xavie\\Documents\\BRIDGE\\AI\\YOLO\\training\\backup-52-yolo4-american1sym--no-rand-2020.12.16\\cardsets_scenes\\cardset-american1sym--no-rand-scenes-52\\check000920500.jpg"
    
    
    cv_image = cv2.imread(image_name)
        

    image2 = QtGui.QImage(image_name)
    #ff = image2.format()
    image2_ptr = image2.constBits()
        
    image2_ptr_arr = np.array(image2_ptr).reshape(750, 750, 4)

    for i in range(750):
        for j in range(750):
            #print("---------------------------------")
            dat1 = cv_image[i][j]
            dat2 = image2_ptr_arr[i][j]

            r_ok = dat1[0] == dat2[0]
            g_ok = dat1[1] == dat2[1]
            b_ok = dat1[2] == dat2[2]
            
            if (not r_ok) or (not g_ok) or (not b_ok):
                print("---------------------------------")
                print(dat1)
                print(dat2)
        

    #image3 = image2.convertToFormat(QtGui.QImage.Format.Format_RGB888)
    image3 = image2.convertToFormat(QtGui.QImage.Format.Format_BGR888)
    image3_ptr = image3.constBits()
    # strange, 2 bits added at each line -> 750*2 = 1500 bits too much  ?????
    image3_ptr_arr = np.array(image3_ptr).reshape(563000, 3)  #  Copies the data


    for i in range(750):
        for j in range(750):

            k = 750*i + j

            #print("---------------------------------")
            dat2 = image2_ptr_arr[i][j]
            dat3 = image3_ptr_arr[k]

            r_ok = dat2[0] == dat3[0]
            g_ok = dat2[1] == dat3[1]
            b_ok = dat2[2] == dat3[2]

            if (not r_ok) or (not g_ok) or (not b_ok):
                print("---------------------------------", k, i, j)
                print("dat2", dat2)
                print("dat3", dat3)


        
if __name__ == '__main__':
    main()