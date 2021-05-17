from pypot.primitive import LoopPrimitive
from pypot.primitive.utils import Sinus
from pypot.creatures import PoppyErgoJr


class Dance(LoopPrimitive):
    def __init__(self, robot):
        LoopPrimitive.__init__(self, robot, 1.)

    def setup(self):
        for m in self.robot.motors:
            m.compliant = False

        self.move_freq = 0.5
        self.sinus = [
            Sinus(self.robot, 25., [self.robot.m6], amp=30., freq=self.move_freq),
            Sinus(self.robot, 25., [self.robot.m5], amp=30., freq=self.move_freq),
            Sinus(self.robot, 25., [self.robot.m4], amp=15., freq=self.move_freq),
            Sinus(self.robot, 25., [self.robot.m3], amp=5., freq=self.move_freq),
            Sinus(self.robot, 25., [self.robot.m2], amp=10., freq=self.move_freq),
            Sinus(self.robot, 25., [self.robot.m1], amp=15., freq=self.move_freq),

            # Sinus(self.robot, 25., [self.robot.m5], amp=30, freq=.8),
            # Sinus(self.robot, 25., [self.robot.m6], amp=30, freq=.8, phase=180),

            # Sinus(self.robot, 25., self.robot.motors, amp=10, freq=.1)
        ]

        self.init_pos = {
            'm1': 0.0,
            'm2': -110.,
            'm3': 65.0,
            'm4': 0.0,
            'm5': 34.0,
            'm6': 20.0,
        }

        #dict([(m.name, 0.0) for m in self.robot.motors])
        self.robot.goto_position(self.init_pos, 1., wait=True)

        for m in self.robot.motors:
            m.moving_speed = 30.#15.

        for m in self.robot.motors:
            m.led = 'green'

        [s.start() for s in self.sinus]

    def update(self):
        pass

    def teardown(self):
        [s.stop() for s in self.sinus]

        self.robot.goto_position(self.init_pos, 3., wait=True)

        for m in self.robot.motors:
            m.led = 'off'

if __name__ == '__main__':
    robot = PoppyErgoJr(config='config_new.json')
    dance = Dance(robot)
    dance.start()
    q = input()
    dance.stop()

