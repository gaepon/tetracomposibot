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
        self.bMethods = [self.hateWallTraining, self.loveEnemyBotTraining, self.hateWall2, self.sub]
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

    def stay(self, sensors, sensor_view=None, sensor_to_robot=None, sensor_to_wall=None, sensor_robot=None, sensor_team=None):
        return 0,0

    def genetic(self, sensors, sensor_view=None, sensor_to_robot=None, sensor_to_wall=None, sensor_robot=None, sensor_team=None):
        #param_trans = [0.3990626228373406, 0.130909966267728, 0.3973892760930806, 0.5195417448674287, -0.998824923203858, 0.5615106705907513, 0.29709583175249654, -0.15436122863294877, -0.8468911421793281, -0.7807404888752585, 0.3796389006756662, -0.027098545325070944, 0.12016350586850466, -0.47293278817578166, -0.6128695349817537, -0.7281828903595962, 0.7975742276444755]
        #param_rot = [-0.3285939132723319, 0.16645761938370485, 0.6805356775974944, -0.28172241059761904, 0.6942858730409815, -0.11632718117248264, 0.6930638047437245, 0.653362047648449, 0.5124001442546682, 0.3923162072821662, 0.08442369493138302, -0.34846582328460696, -0.9191888611833168, -0.6186783398041478, -0.15881206269701442, 0.05787387617175166, 0]
        param_trans = [-0.6804762101671082, 0.9199277086833919, 0.8786540669737521, 0.8242153800229013, 0.5851863604473733, -0.983221298371439, -0.6839153687088202, -0.9851869390577392, 0.36231944861004584, 0, -0.21321907856762268, 0, 0.4259291293757661, 0.9204860211933605, 0.3349192763185205, 0.12938450061865936, -0.6609154078986028]
        param_rot = [-0.9049898885556076, 0, 0.3988513043417172, 0.9374433064238867, 0, 0, 0.04011890146516417, 0, 0, 0, -0.9271351103651484, 0.4428255896789961, 0, -0.44525968093167845, 0.18509207135230654, 0, 0]

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
        behaviours = [self.sub, self.hateWall2, self.hateWall2, self.genetic]

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

