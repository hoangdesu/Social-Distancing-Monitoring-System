import time
from grove.gpio import GPIO
import peopleInRoom


class GroveMiniPIRMotionSensor(GPIO):
    count = 0

    def __init__(self, pin):
        super(GroveMiniPIRMotionSensor, self).__init__(pin, GPIO.IN)
        self._on_detect = None

    @property
    def on_detect(self):
        return self._on_detect

    @on_detect.setter
    def on_detect(self, callback):
        if not callable(callback):
            return

        if self.on_event is None:
                self.on_event = self._handle_event

        self._on_detect = callback

    def _handle_event(self, pin, value):
        if value:
            peopleInRoom.leavingNoQR = 1
            self.count = self.count + 1
            if peopleInRoom.leavingDect is 1:
                peopleInRoom.leavingNoQR = 0
                peopleInRoom.pp = peopleInRoom.pp - 1
                peopleInRoom.leavingDect = 0
                peopleInRoom.leavingUpdate = 1
                print("Number of people in the room: {}".format(peopleInRoom.pp))
            if callable(self._on_detect):
                self._on_detect()
                

def main():
    pir = GroveMiniPIRMotionSensor(22)

    def callback():
        print("The number of people who passed this area: {}".format(pir.count))

    pir.on_detect = callback

    while True:
        time.sleep(0.1)


#if __name__ == '__main__':
#   main()