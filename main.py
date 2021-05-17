

from pypot.creatures import PoppyErgoJr
from pypot.primitive import LoopPrimitive
#from poppy_ergo_jr.postures import IdleBreathing
from poppy_ergo_jr.primitives.postures import CuriousPosture
from poppy_ergo_jr.primitives.postures import IdleBreathing
from poppy_ergo_jr.primitives.dance import Dance


#robot = PoppyErgoJr(simulator='poppy-simu')
robot = PoppyErgoJr(config='config_new.json',use_snap=True)
dance = Dance(robot)
# dance.start()
# dance.stop()

breathing = IdleBreathing(robot, 1.)
c = CuriousPosture(robot,1.)
        
for i in [1]:
    breathing.start()
    breathing.stop()
    c.start()
    c.stop()
for i in [1,2,3,4,5,6,7]:
    breathing.start()
    breathing.stop()
