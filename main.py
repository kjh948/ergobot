

from pypot.creatures import PoppyErgoJr
from pypot.primitive import LoopPrimitive
#from poppy_ergo_jr.postures import IdleBreathing
from poppy_ergo_jr.primitives.postures import CuriousPosture
from poppy_ergo_jr.primitives.postures import IdleBreathing
from poppy_ergo_jr.primitives.dance import Dance


#robot = PoppyErgoJr(simulator='poppy-simu')
robot = PoppyErgoJr(config='config_new.json')
dance = Dance(robot)
dance.start()

# breathing = IdleBreathing(robot, 1.)
# breathing.start()

# c = CuriousPosture(robot,1.)
# c.start()

#robot.dance.stop()
#breathing = IdleBreathing(robot, 1.)
#breathing.start()
