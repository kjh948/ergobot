import time
import random
import cv2
import numpy as np

from pypot.primitive import Primitive, LoopPrimitive

from pypot.primitive.move import MoveRecorder
from pypot.primitive.move import MovePlayer
from pypot.creatures import PoppyErgoJr

class BaseDemo(LoopPrimitive):
    #je définit ma class BaseDemo, fille de la class Primitive, et futur mère ;)
    def __init__(self, robot):
        #je définit ma fonction __init__()
        Primitive.__init__(self, robot)
        #j'apel la fonction __init__ de ma class mère

        self.defaut_posture = [0, -45, 25, 0, 45, -25]
        #je définit un nouveau attribue

    def posture_is(self, posture, error=2, motors='all'):
        if motors == 'all' : motors= self.robot.motors
        for i in range(len(motors)):
            if abs( motors[i].present_position - posture[i] ) > error : return False
        return True

    def distance_with(self, posture, motors='all'):
        #retourne une liste contenant la difference en degres (pour chaque moteur) entre la position actuelle du robot et une position donnee
        if motors == 'all': motors= self.robot.motors
        output= [ abs( motors[i].present_position - posture[i] ) for i in range(len(motors)) ]
        '''
        autre ecriture:
        output=[]
        for i in range(len(motors)):
            output.append( abs( motors[i].present_position - posture[i] )
        '''
        return output

    def sleep_except_should_stop(self, time_seconde):
        for i in range (int(time_seconde*10)):
            if not self.should_stop(): time.sleep(time_seconde/(time_seconde*10))
            #si l'on ne demande pas d'arréter la primitive, on attend

    def countdown(self, time_seconde):
        for i in range(int(time_seconde+time_seconde*0.2)):

            if not self.should_stop():
                #si l'on ne demande pas d'arréter la primitive
                if self.should_pause(): self.wait_to_resume()
                #si on me demande pause, j'attend jusqu'a reprise

                for m in self.robot.motors: m.led="off"
                time.sleep( 0.5- (0.3/(time_seconde+time_seconde*0.2) *i ))
                for m in self.robot.motors: m.led="green"
                time.sleep(0.5)
        #je créer une sorte de compte a reboug lumineux

    def setup(self):
        #je définit la fonction setup()
        duration= int( max( self.distance_with( self.defaut_posture ) ) ) /100.
        #temps en fonction de la distance maximal actuel ; soit une distance max (thèorique) de 180° exécuter en un temps de 1,8 seconde ; connaissance ma position_défaut la distance max est 150° (avec m2) donnant un temps max de 1,5 secondes pour reprendre sa positon. on à donc le temps qui varie en fonction de la distance, c'est donc la vitesse qui est fixe. V=D/T ; 150/1,5=100 ; le moteur le plus éloigner de sa postion defaut se déplace à 100°/sec ; les autre moteurs ajuste leur vitesse (ralentissent) pour arriver à leur position defaut en même temps que le moteur le plus éloigné.
        for m in self.robot.motors:
            m.compliant=False
            m.goto_position( self.defaut_posture[m.id-1] , duration )
        time.sleep( duration + 0.2 )
        #déplacer les moteurs vers leur position defaut (définit dans self.__init__)
        for m in self.robot.motors:
            m.compliant=True
            m.led='off'
        time.sleep(0.1)
        #mettre tout les moteurs en "souple" et éteindre les led

    def run(self):
        pass
    #je ne définit pas de fonction run() ; elle sera définit dans mes class filles

    def teardown(self):
        #je définit la fonction teardown()
        BaseDemo.setup(self)
        #j'appel BaseDemo.setup() : le robot éffectue la même action qu'au démarage

class Tinsel(Primitive): #on crée un nouvelle class Tinsel qui hérite de la class Primitive
    '''
    ici on veut que l'ergo glignote, qu'on puisse lui spécifier les couleurs et la vitesse (en Hz)
    - Toute les fonctions qui ne sont pas rédéfinit ici sont hérité de la class Primitive
    - La fonction __init__() est exécute des que la class est instancier
    - Ici nous souhaitons ajouter deux variables non définit dans la class Primitive: les couleurs et la vitesse
    '''
    def __init__(self,robot,colors=['green','red','yellow','blue','pink','cyan','white','off'],freq=2):
        #on redéfinit la fonction __init__() hérité de Primitive, et lui ajoute deux parametre: colors et freq
        Primitive.__init__(self,robot)
        #on appel la fonction __init__() de la class Primitive (pour que les autres variables et parametre de celle-ci s'initie correctement)
        self.colors=colors
        self.freq=freq
        #on définit l'attribut self.colors et self.freq (qui peuvent être vue comme des variables) qui contiennent respectivement les couleurs spécifier dans le parametre colors et la vitesse spécifier dans le parametre freq passer lors l'instanciation de la primitive

    def run(self):
        #on définit la fonction run()
        while not self.should_stop():
            #tant que l'on ne demande pas d'arréter la primitive
            for color in self.colors:
                #pour chacune des couleurs
                if not self.should_stop():
                    #si l'on ne demande pas d'arréter la primitives
                    if self.should_pause(): self.wait_to_resume()
                    #si on me demande pause, j'attend jusqu'a reprise
                    for m in self.robot.motors: m.led = color
                    #pour chaque moteurs, mettre la led en la couleur
                    for i in range(5):
                        if not self.should_stop():
                            if self.should_pause(): self.wait_to_resume()
                            time.sleep((1./self.freq)/5)
                    #je vérife dix foi par période si l'on ne demande pas d'arréter la primitives


class ProgByDemo(BaseDemo, Primitive):

    def __init__(self, robot, record_time=10):
        BaseDemo.__init__(self, robot)
        self.robot.attach_primitive(Tinsel(self.robot), 'tinsel')
        self.record_time=record_time # en seconde

    def run(self):
        while not self.should_stop():
            if self.should_pause(): self.wait_to_resume()

            while not(self.posture_is(self.defaut_posture)): time.sleep(0.1)
            for m in self.robot.motors:
                m.led="green"
                m.compliant=True

            my_record = MoveRecorder(self.robot, 50, self.robot.motors)
            my_record.start()

            sleep = int(self.record_time+(self.record_time/5.))
            for i in range(sleep):
                if not self.should_stop():
                    if self.should_pause(): self.wait_to_resume()
                    for m in self.robot.motors: m.led="green"
                    time.sleep(0.5)
                    for m in self.robot.motors: m.led="off"
                    time.sleep(0.5-((0.5/sleep)*i))

            my_record.stop()
            #my_record.wait_to_stop()

            if not self.should_stop():
                if self.should_pause(): self.wait_to_resume()

                self.robot.tinsel.colors=['red']
                self.robot.tinsel.freq=1
                self.robot.tinsel.start()

                self.robot._primitive_manager.remove(self)
                # patch pour passer des fake moteurs de la primitive ProgByDemo aux moteurs reel de l ergo

                my_play = MovePlayer(self.robot, my_record.move)
                my_play.start()

                for t in range(self.record_time*2):
                    if not self.should_stop():
                        if self.should_pause(): self.wait_to_resume()
                        time.sleep(0.5)

                if my_play.is_alive(): my_play.stop()

                self.robot.tinsel.stop()

                self.robot._primitive_manager.add(self) # on redonne le control des moteurs a la primitive ProgByDemo

                duration= int( max( self.distance_with( self.defaut_posture ) ) )/100.
                for m in self.robot.motors:
                    m.compliant=False
                    m.goto_position(self.defaut_posture[m.id-1],duration)
                time.sleep(duration)


if __name__ == '__main__':
    robot = PoppyErgoJr(config='config_new.json')
    teach = ProgByDemo(robot)
    teach.start()
    q = input()
    teach.stop()
