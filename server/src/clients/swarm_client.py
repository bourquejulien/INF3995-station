import time

import cflib.crtp
from cflib.positioning.motion_commander import MotionCommander

from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie


class SwarmClient:
    Uris = [
        'radio://0/80/2M/E7E7E7E751',
        'radio://0/80/2M/E7E7E7E752'
    ]

    def __init__(self, uri):
        self.scf = SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache'))

    def __enter__(self):
        cflib.crtp.init_drivers()
        self.scf.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.scf.__exit__(exc_type, exc_val, exc_tb)

    def blink(self, rounds=20, delay=0.05):
        for i in range(rounds):
            self.scf.cf.param.set_value('led.onoff', 1)
            time.sleep(delay)
            self.scf.cf.param.set_value('led.onoff', 0)
            time.sleep(delay)

        self.scf.cf.param.set_value('led.bitmask', 0)

    def demo(self, height=0.2):
        with MotionCommander(self.scf, default_height=height) as mc:
            time.sleep(0.5)
            mc.forward(0.5)
            time.sleep(0.5)
            mc.back(0.5)
            time.sleep(0.5)
