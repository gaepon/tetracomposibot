
from robot import * 

nb_robots = 0
debug = True

class Robot_player(Robot):

    team_name = "The Otter Team"
    robot_id = 3
    iteration = 0

    def __init__(self, x_0, y_0, theta_0, param_trans, param_rot, name="n/a", team="n/a"):
        global nb_robots
        if team != "n/a":
            self.team_name = team
        self.robot_id = nb_robots
        self.param_trans = param_trans
        self.param_rot = param_rot
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
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
        
        translation = self.param_trans[0]
        rotation = self.param_rot[0]

        for i in range(len(sensor_to_robot)):
            translation += sensor_to_wall[i]*self.param_trans[i+1]
            rotation += sensor_to_wall[i]*self.param_rot[i+1]
        for i in range(len(sensor_to_robot)):
            translation += sensor_to_robot[i]*self.param_trans[i+len(sensor_to_wall)+1]
            rotation += sensor_to_robot[i]*self.param_rot[i+len(sensor_to_wall)+1]
        
        return translation, rotation, False
