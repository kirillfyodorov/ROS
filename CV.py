#!/usr/bin/env python

import cv2 as cv
import numpy as np
import video
import math
import os
import time
import rospy
from std_msgs.msg import String


if __name__ == '__main__':
    cv.namedWindow("result")
    cap = video.create_capture(1)

    path = 'IMG'

    hsv_min = np.array((36, 35, 103), np.uint8)
    hsv_max = np.array((87, 117, 208), np.uint8)

    color_blue = (255, 0, 0)
    color_red = (0, 0, 128)
    i = 1
    while True:
        flag, img = cap.read()
        img = cv.flip(img, 1)
        width = np.size(img, 1)
        try:
            hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV )
            thresh = cv.inRange(hsv, hsv_min, hsv_max)
            contours0, hierarchy = cv.findContours( thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

            for cnt in contours0:
                rect = cv.minAreaRect(cnt)
                box = cv.boxPoints(rect)
                box = np.int0(box)
                center = (int(rect[0][0]), int(rect[0][1]))
                area = int(rect[1][0]*rect[1][1])


                if area > 80000:
                    cv.drawContours(img,[box],0,color_blue,2)
                    cv.circle(img, center, 5, color_red, 2)
                    cv.putText(img, "%d" % (center[1]), (center[0]+20, center[1]), cv.FONT_HERSHEY_SIMPLEX, 1, color_red, 2)
                    cv.putText(img, "%d" % (center[0]), (center[0] + 20, center[1] - 40), cv.FONT_HERSHEY_SIMPLEX, 1,
                               color_red, 2)
                    if((width/2 - center[0] < 50 and width/2 - center[0] > 0) or (width/2 - center[0] > -50 and width/2 - center[0] < 0)):
                        #cv.imwrite(os.path.join(path, 'test-{id}.jpg'.format(id=i)), img)

                        time.sleep(2)

                        pub = rospy.Publisher('imgpath', String, queue_size=1)
                        rospy.init_node('CV')
                        pub.publish(os.path.join('test-{id}.jpg'.format(id=i)))
                        i += 1

            cv.imshow('result', img)
        except:
            cap.release()
            raise
        ch = cv.waitKey(5)
        if ch == 27:
            break

    cap.release()
    cv.destroyAllWindows()
