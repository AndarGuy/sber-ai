from threading import Thread

import cv2


class Test:
    def __init__(self):
        self.stream = cv2.VideoCapture(0)
        self.frame = 0
        self.stopped = False
        th1 = Thread(target=self.test, daemon=True, name='th1', args=())
        th1.start()

        while True:
            print(self.frame)
            cv2.imshow("Video", self.frame)

            if (cv2.waitKey(1) == ord("q")):
                break

    def test(self):
        while not self.stopped:
            self.grabbed, self.frame = self.stream.read()
            if cv2.waitKey(1) == ord("q"):
                self.stopped = True


Test()
