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

    team_name = "The Otter Team"  # vous pouvez modifier le nom de votre équipe
    robot_id = -1             # ne pas modifier. Permet de connaitre le numéro de votre robot.
    memory = 0                # vous n'avez le droit qu'a une case mémoire qui doit être obligatoirement un entier

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
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

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        behaviours = [self.sub, self.hateWall2, self.hateWall2, self.stay]

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
        
        translation, rotation = behaviours[self.id-1](sensors, sensor_view, sensor_to_robot, sensor_to_wall, sensor_robot, sensor_team)

        return translation, rotation, False

