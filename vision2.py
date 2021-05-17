import sys
import cv2
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
import time

import os
from multiprocessing import Process, Queue
import logging

logging.basicConfig(level=logging.INFO)

min_size = (30, 30)
image_scale = 2
haar_scale = 1.2
min_neighbors = 5
haar_flags = 0

mode='face'
path = 'haarcascade_frontalface_alt2.xml'

model = cv2.CascadeClassifier(path)
vs = cv2.VideoCapture(0)#VideoStream(src=0).start()
#sleep(2.0)
fps = FPS().start()
isDetected = None


def detect(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    gray = cv2.resize(gray, (0, 0), fx=0.5, fy=0.5)
    faces = model.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=min_neighbors,
        minSize=min_size,
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    if faces is not None:
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (2 * x, 2 * y), (2 * (x + w), 2 * (y + h)), (0, 255, 0), 2)
    cv2.imshow("video", frame)
    fps.update()
    return faces


def process():
    t = cv2.getTickCount()
    _,frame = vs.read()
    ret = detect(frame)
    t = cv2.getTickCount() - t
    print("time taken for detection = %gms" % (t / (cv2.getTickFrequency() * 1000.)))
    return ret


def loop(msg=None):
    while 1:
        ret = process()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if len(ret) > 0:
            msg.put(ret)
            # self.isDetected = ret
            logging.info('.')
        else:
            isDetected = None
        #     msg.put(ret)


class r2d2Vision(object):
    def __init__(self, mode='face', path = 'resources/haarcascade_frontalface_alt2.xml'):
        pass
    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        gray = cv2.resize(gray, (0, 0), fx=0.5, fy=0.5)
        faces = self.model.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=min_neighbors,
            minSize=min_size,
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        if faces is not None:
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (2*x, 2*y), (2*(x + w), 2*(y + h)), (0, 255, 0), 2)
        cv2.imshow("video", frame)
        self.fps.update()
        return faces

    def process(self):
        t = cv2.getTickCount()
        frame = self.vs.read()
        ret = self.detect(frame)
        t = cv2.getTickCount() - t
        print("time taken for detection = %gms" % (t / (cv2.getTickFrequency() * 1000.)))
        return ret

    def loop(self, msg=None):
        while 1:
            ret = self.process()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if len(ret)>0:
                msg.put(ret)
                self.isDetected = ret
                #logging.info('.')
            else:
                self.isDetected = None
            #     msg.put(ret)

if __name__ == "__main__":
    msg = Queue()
    #vis = r2d2Vision()

    proc = Process(target=loop, args=(msg,))
    #proc = Process(target=vis.loop())

    proc.start()
    while 1:
        try:
            res = msg.get(timeout=1)
            if res is not None:
                print(res)
                logging.info('detected')
        except:
            break

    proc.join()
    #vis.fps.stop()
    print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # do a bit of cleanup
    cv2.destroyAllWindows()
    #vis.vs.stop()
