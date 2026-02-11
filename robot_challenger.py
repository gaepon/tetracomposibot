# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiant/e : Jules Rousseaux 21210789
#  Prénom Nom No_étudiant/e : Haroun Zerdoumi 21212992
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

from robot import * 

nb_robots = 0

class Robot_player(Robot):

    team_name = "A"  # vous pouvez modifier le nom de votre équipe
    robot_id = -1             # ne pas modifier. Permet de connaitre le numéro de votre robot.
    memory = 0                # vous n'avez le droit qu'a une case mémoire qui doit être obligatoirement un entier

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a", b=None):
        global nb_robots
        if team != "n/a":
            self.team_name = team
        self.bMethods = [self.hateWallTraining, self.loveEnemyBotTraining, self.hateWall2, self.sub, self.comportement_zigzag]
        self.robot_id = nb_robots
        self.b = b
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

    def hateFriends(self,sBot, sTeam):
        front_right=0 if sTeam[sensor_front_right]!=self.team_name else sBot[sensor_front_right]*1.4
        front_left=0 if sTeam[sensor_front_left]!=self.team_name else sBot[sensor_front_left]*-1.4
        return sBot[sensor_front]*-.5-0.1, front_right+front_left

    def hateWall(self, sWall):
        return sWall[sensor_front]*.5+0.1, sWall[sensor_front_right]*-1.4+sWall[sensor_front_left]*1.4+0.01

    def loveEnemyBot(self, sBot, sTeam):
        front_right=0 if sTeam[sensor_front_right]==self.team_name else sBot[sensor_front_right]*1.4
        front_left=0 if sTeam[sensor_front_left]==self.team_name else sBot[sensor_front_left]*-1.4
        return sBot[sensor_front]*.5+0.1, front_right+front_left

    def checkFriendOrFoe(self, sTeam):
        sTeamFront=sTeam[sensor_front], sTeam[sensor_front_left], sTeam[sensor_front_right]
        for t in sTeamFront:
            if t not in ['n/a', self.team_name]:
                return 1
            if t==self.team_name:
                return -1
        return 0
    
    def hateWall2(self, sensors, sensor_view=None, sensor_to_robot=None, sensor_to_wall=None, sensor_robot=None, sensor_team=None):
        sWall = sensor_to_wall
        return sWall[sensor_front]*.5+0.1, sWall[sensor_front_right]*-1.4+sWall[sensor_front_left]*1.4+(random.random()-0.5)

    def sub(self, sensors, sensor_view=None, sensor_to_robot=None, sensor_to_wall=None, sensor_robot=None, sensor_team=None):
        if self.checkFriendOrFoe(sensor_team)==1:
            translation, rotation = self.loveEnemyBot(sensor_to_robot, sensor_team)
        elif self.checkFriendOrFoe(sensor_team)==-1:
            translation, rotation = self.hateFriends(sensor_to_robot, sensor_team)
        else:
            translation, rotation = self.hateWall(sensor_to_wall)
        return translation, rotation

    def comportement_zigzag(self, sensors, sensor_view=None,
                      sensor_to_robot=None, sensor_to_wall=None,
                      sensor_robot=None, sensor_team=None):
        """
        Comportement zigzag :
        - Avance tout droit.
        - Si mur DEVANT: print("mur"), puis exécute un cycle :
            (tour -> avance N -> tour) dans un sens donné.
        - Après un cycle complet, le prochain cycle se fera dans l'autre sens
        (gauche puis droite puis gauche...).
        - Pendant l'avance (state 2), si mur DEVANT: print("mur") et on relance
        immédiatement un nouveau cycle (dans le sens actuel).

        Concrétement le robot fait des zig-zag vers le haut (de notre point de vue),
        quand il rencontre le mur du haut, il fait des zig-zag vers la droite, etc...

        Attention : nous vous conseillons de lire comment nous nous sommes servis de 
        la mémoire plus loin dans les commentaires.
        """

        V_FWD = 1.0         #vitesse vers l'avant
        W = 1.0             # vitesse angulaire 
        EPS = 0.12          # seuil collision/proximité (trouvé à 0.1111...)
        N = 4               # steps d'avance dans le cycle (trouvé à 4)
        K_TURN = 9          # steps de rotation (trouvé à 9)

        """Problème avec la mémoire : nous avons trois éléments à retenir (direction, état, step)
        Or nous n'avons qu'un seul bloc mémoire entier (qui n'a pas de limite de taille cependant)

        Nous nous sommes donc inspiré de la lecture mémoire vu dans l'UE d'architecture des ordinateurs :
        memory = dir * 100000 + state * 1000 + counter

        dir * 100000 met dir dans les centaines de milliers (le “bloc lourd”, ce ne sont pas des bits comme
        en architecture mais la logique en la même en base 10)
        state * 1000 met state dans les milliers
        counter occupe les unités (0 à 999)

        Par exemple dir = 1, state = 2, counter = 17
        memory = 1*100000 + 2*1000 + 17 = 102017
        Ça veut dire : “droite, état 2, il reste 17 pas”. On peut facilement le retrouver à partir de la
        valeur de memory

        dir: 0=gauche, 1=droite
        state: 0=avance libre, 1=tour1, 2=avance N, 3=tour2
        counter: steps restants
        """

        if not hasattr(self, "memory"):         #cas initiale
            self.memory = 0                     # dir=0, state=0, counter=0

        dir = self.memory // 100000            #On retrouve la direction
        rest = self.memory % 100000             
        state = rest // 1000                    #On retrouve l'état
        counter = rest % 1000                   #On retrouve le compteur de pas restant

        # sécurité
        if sensor_view is None:
            return V_FWD, 0.0

        #Fonction pour détecter le mur    
        def mur_devant():                       
            return (sensor_view[sensor_front] == 1) and (sensors[sensor_front] <= EPS)

        #Fonction pour calculer la mémoire
        def set_mem(new_dir, new_state, new_counter):   
            self.memory = new_dir * 100000 + new_state * 1000 + new_counter

        #Fonction de choix de la rotation
        def rot_cmd():
            # gauche: +W ; droite: -W
            return (W if dir == 0 else -W)

        # --------- STATE 0 : AVANCE LIBRE ----------
        if state == 0:
            if mur_devant():                #On passe au state suivant que s'il rencontre un mur
                #print("mur")
                set_mem(dir, 1, K_TURN)
                return 0.0, rot_cmd()       #Auquel cas il tourne    
            return V_FWD, 0.0               #Sinon il avance

        # --------- STATE 1 : TOUR 1 ----------
        if state == 1:
            if counter > 1:                 #On détermine où il en est dans la rotation grâce au compteur de pas
                set_mem(dir, 1, counter - 1)
                return 0.0, rot_cmd()       #Si ce n'est pas suffisant on continue à tourner
            else:
                set_mem(dir, 2, N)          #Passe à l'avance N
                return V_FWD, 0.0

        # --------- STATE 2 : AVANCE N ----------
        if state == 2:
            if mur_devant():                #S'il atteint un bord
                #print("mur")
                set_mem(dir, 1, K_TURN)     #On change de zig-zag
                return 0.0, rot_cmd()

            if counter > 1:                 #On avance de façon fixe cette fois
                set_mem(dir, 2, counter - 1)
                return V_FWD, 0.0           
            else:
                set_mem(dir, 3, K_TURN)     # tour2
                return 0.0, rot_cmd()

        # --------- STATE 3 : TOUR 2 ----------
        if state == 3:
            if counter > 1:                 #Même schéma qu'au tour 1
                set_mem(dir, 3, counter - 1)
                return 0.0, rot_cmd()
            else:
                # fin du cycle: on repasse en avance libre
                # et on inverse le sens pour le prochain mur (gauche <-> droite)
                new_dir = 1 - dir
                set_mem(new_dir, 0, 0)
                return V_FWD, 0.0

        #sécurité
        #set_mem(dir, 0, 0)
        #return V_FWD, 0.0

    def genetic(self, sensors, sensor_view=None, sensor_to_robot=None, sensor_to_wall=None, sensor_robot=None, sensor_team=None):
        #param_trans = [0.3990626228373406, 0.130909966267728, 0.3973892760930806, 0.5195417448674287, -0.998824923203858, 0.5615106705907513, 0.29709583175249654, -0.15436122863294877, -0.8468911421793281, -0.7807404888752585, 0.3796389006756662, -0.027098545325070944, 0.12016350586850466, -0.47293278817578166, -0.6128695349817537, -0.7281828903595962, 0.7975742276444755]
        #param_rot = [-0.3285939132723319, 0.16645761938370485, 0.6805356775974944, -0.28172241059761904, 0.6942858730409815, -0.11632718117248264, 0.6930638047437245, 0.653362047648449, 0.5124001442546682, 0.3923162072821662, 0.08442369493138302, -0.34846582328460696, -0.9191888611833168, -0.6186783398041478, -0.15881206269701442, 0.05787387617175166, 0]
        #param_trans = [-0.6804762101671082, 0.9199277086833919, 0.8786540669737521, 0.8242153800229013, 0.5851863604473733, -0.983221298371439, -0.6839153687088202, -0.9851869390577392, 0.36231944861004584, 0, -0.21321907856762268, 0, 0.4259291293757661, 0.9204860211933605, 0.3349192763185205, 0.12938450061865936, -0.6609154078986028]
        #param_rot = [-0.9049898885556076, 0, 0.3988513043417172, 0.9374433064238867, 0, 0, 0.04011890146516417, 0, 0, 0, -0.9271351103651484, 0.4428255896789961, 0, -0.44525968093167845, 0.18509207135230654, 0, 0]
        param_trans = [0.08880227092481685, -0.6298933958153448, 0, 0, 0, 0.5502360828692574, -0.7428804978679167, 0, 0, 0.5139006141821487, 0, -0.895733219225612, 0, -0.14307661107099268, 0.13271635932685677, 0, -0.2727047425916629]
        param_rot = [-0.0009223214112707989, -0.7310838256556387, 0, -0.08878317063512808, -0.2919920912142979, -0.5506646517057954, 0, -0.32388615157244605, 0.4294876747950438, 0.09886850900905197, -0.2868432615776686, 0.2931164263737305, -0.9829958610261431, -0.010937058707369607, -0.9140148757174713, 0.441503637784056, -0.33718594046662953]

        translation = param_trans[0]
        rotation = param_rot[0]

        for i in range(len(sensor_to_robot)):
            translation += sensor_to_wall[i]*param_trans[i+1]
            rotation += sensor_to_wall[i]*param_rot[i+1]
        for i in range(len(sensor_to_robot)):
            translation += sensor_to_robot[i]*param_trans[i+len(sensor_to_wall)+1]
            rotation += sensor_to_robot[i]*param_rot[i+len(sensor_to_wall)+1]
        
        return translation, rotation


    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        behaviours = [self.sub, self.hateWall2, self.comportement_zigzag, self.genetic]

        sensor_to_wall = []
        sensor_to_robot = []
        for i in range (0,8):
            if  sensor_view[i] == 1:
                sensor_to_wall.append( sensors[i] )
                sensor_to_robot.append(1.0)
            elif  sensor_view[i] == 2:
                sensor_to_wall.append( 1.0 )
                sensor_to_robot.append( sensors[i] )
            else:
                sensor_to_wall.append(1.0)
                sensor_to_robot.append(1.0)
        
        if self.b==None:
            translation, rotation = behaviours[self.id-1 % 4](sensors, sensor_view, sensor_to_robot, sensor_to_wall, sensor_robot, sensor_team)
        else:
            translation, rotation = self.bMethods[int(self.b)](sensors, sensor_view, sensor_to_robot, sensor_to_wall, sensor_robot, sensor_team)

        return translation, rotation, False
    
    # The Following Behaviours were added as part of the genetic algorithm's training to increase diversity and can be deleted without worry once the training is complete

    def hateWallTraining(self, sensors, sensor_view=None, sensor_to_robot=None, sensor_to_wall=None, sensor_robot=None, sensor_team=None):
        sWall = sensor_to_wall
        return sWall[sensor_front]*.5+0.1, sWall[sensor_front_right]*-1.4+sWall[sensor_front_left]*1.4+0.01

    def loveEnemyBotTraining(self, sensors, sensor_view=None, sensor_to_robot=None, sensor_to_wall=None, sensor_robot=None, sensor_team=None):
        sTeam = sensor_team
        sBot = sensor_to_robot
        front_right=0 if sTeam[sensor_front_right]==self.team_name else sBot[sensor_front_right]*1.4
        front_left=0 if sTeam[sensor_front_left]==self.team_name else sBot[sensor_front_left]*-1.4
        return sBot[sensor_front]*.5+0.1, front_right+front_left

