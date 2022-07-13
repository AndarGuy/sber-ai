import time
from threading import Thread

import cv2
#import serial

import road_detection
import sign_detection
import traffic_light_detection

port = '/dev/ttyUSB0'

cap_sign = cv2.VideoCapture(0)
cap_road = cv2.VideoCapture(1)
#out = serial.Serial(port, 115200)

#out.write(b'P0')


class Event:
    def __init__(self, type, direction, duration, value):
        self.time_start = time.time()
        self.time_end = self.time_start + duration
        self.type = type
        self.direction = direction
        self.value = value

    def get_time_start(self):
        return self.time_start

    def get_time_end(self):
        return self.time_end

    def get_type(self):
        return self.type

    def get_direction(self):
        return self.direction

    def get_value(self):
        return self.value


class Car:
    def __init__(self, possible_signs, debug=True, default_speed=9):

        self.traffic_light_thread = Thread(name='traffic_light_thread', target=self.traffic_light_reaction, daemon=True)
        self.signs_thread = Thread(name='sings_thread', target=self.sign_reaction, daemon=True)
        self.road_thread = Thread(name='road_thread', target=self.road_reaction, daemon=True)

        self.default_speed = default_speed
        self.speed = default_speed
        self.stopped = False
        self.signs_log = []
        self.turn = None
        self.last_sign_search = time.time()
        self.debug = debug
        self.possible_signs = possible_signs
        self.quit = False
        self.deviation = None
        self.active_event = None  # (time_start, time_end, type, direction, value)

    def start(self):
        self.traffic_light_thread.start()
        self.signs_thread.start()
        self.road_thread.start()

        self.run()

    def run(self):
        while True:
            start_time = time.time()

            if self.active_event and self.active_event.get_time_end() > start_time:
                if self.active_event.get_type() == 'speed':
                    self.speed = self.active_event.get_direction() + self.active_event.get_value()
                elif self.active_event.get_type() == 'turn':
                    self.turn = self.active_event.get_direction() + self.active_event.get_value()

            #out.write(self.turn)
            #out.write(self.speed)

            #print("FPS: ", 1.0 / (time.time() - start_time)) if self.debug and time.time() - start_time else None

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.quit = True
                break

        cap_road.release()
        cap_sign.release()
        cv2.destroyAllWindows()

    def sign_reaction(self):
        print('Sign Thread Start!')
        while True:
            _, frame_sign = cap_sign.read()
            frame_sign = cv2.resize(frame_sign, (720, 480))
            sign = sign_detection.get_sign(frame_sign[0:480, 360:720], self.possible_signs)
            print(sign) if self.debug else None
            if sign:
                if sign_detection.STOP == sign:
                    print("STOP") if self.debug else None
                    self.active_event = Event('speed', 'S', 2, '0')
                elif sign_detection.PEDESTRIAN_CROSSING == sign:
                    print('PEDESTRIAN') if self.debug else None
                    self.active_event = Event('speed', 'F', 2, '3')
                elif sign_detection.LEFT == sign:
                    print('LEFT') if self.debug else None
                    self.active_event = Event('turn', 'L', 0.5, '9')
                elif sign_detection.RIGHT == sign:
                    print('RIGHT') if self.debug else None
                    self.active_event = Event('turn', 'R', 0.5, '9')
                elif sign_detection.FORWARD == sign:
                    print('FORWARD') if self.debug else None
                    self.active_event = Event('turn', 'P', 0.5, '0')
                    pass

            if self.quit:
                break

    def road_reaction(self):
        print('Road Thread Start!')
        while True:
            _, frame_road = cap_road.read()

            self.deviation = road_detection.get_deviation(cv2.resize(frame_road, (60, 45)))

            deviation_value = abs(int(self.deviation * 10))
            if not deviation_value:
                deviation_value = 1

            if self.deviation > 0:
                self.turn = 'L' + str(deviation_value)
            elif self.deviation < 0:
                self.turn = 'R' + str(deviation_value)
            else:
                pass

            if self.quit:
                break

    def traffic_light_reaction(self):
        print('Traffic Light Thread Start!')
        while True:
            _, frame_sign = cap_sign.read()
            #cv2.imshow('traffic', frame_sign[0:480, 360:720]) if self.debug else None
            errors = 0
            red_area = traffic_light_detection.get_traffic_light(frame_sign[0:480, 360:720])['red_traffic']
            dist = 500
            if red_area > dist:
                while errors < 5:
                    if not red_area:
                        errors += 1
                    print('RED!!!', red_area) if self.debug else None
                    #out.write(b'S0')
                    _, frame_sign = cap_sign.read()
                    red_area = \
                        traffic_light_detection.get_traffic_light(cv2.resize(frame_sign, (120, 90))[0:90, 60:120])[
                            'red_traffic']

            if self.quit:
                break


car = Car([sign_detection.STOP, sign_detection.PEDESTRIAN_CROSSING, sign_detection.LEFT, sign_detection.RIGHT,
                  sign_detection.FORWARD], debug=True)
car.start()
