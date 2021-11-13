
from PySide6 import QtCore
from PySide6 import QtGui

import numpy as np
import cv2

def main():
    '''
    '''
    image_name = "test\\2h.png"
    #image_name = "test\\check000968279.jpg"
    
    
    cv_image = cv2.imread(image_name)
        

    image2 = QtGui.QImage(image_name)
    #ff = image2.format()
    image2_ptr = image2.constBits()

    w = image2.width()
    h = image2.height()

    print("image-2: nb bits = %d (%d*%d*4 = %d)" % (len(image2_ptr), w, h, w*h*4))
        
    image2_ptr_arr = np.array(image2_ptr).reshape(h, w, 4)

    for i in range(h):
        for j in range(w):
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
        
    nb_bits_per_line = image2.bytesPerLine()

    #image3 = image2.convertToFormat(QtGui.QImage.Format.Format_RGB888)
    image3 = image2.convertToFormat(QtGui.QImage.Format.Format_BGR888)
    image3_ptr = image3.constBits()

    #print("image-3: nb bits = %d (%d*%d*3 + 1500 = %d)" % (len(image3_ptr), h, w, h*w*3 + h*2))
    print("image-3: nb bits = %d (%d*%d*3 + 600 = %d)" % (len(image3_ptr), h, w, h*w*3 + h*2))

    # strange, 2 bits added at each line -> w*2 = 1500 bits too much  ?????
    # strange, 2 bits added at each line -> w*2 =  600 bits too much  ?????
    image3_ptr_arr = np.array(image3_ptr).reshape(563000, 3) 


    try:
        image3_ptr_arr_xx = np.array(image3_ptr).reshape(h*w, 3)
    except Exception as e:
        print(e)

    for i in range(h):
        for j in range(w):

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
                break


        
if __name__ == '__main__':
    main()