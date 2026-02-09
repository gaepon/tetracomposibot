import subprocess as sp
import random

def createConfig(TheChosenOnes, arena):
    with open("config_training.py") as f:
        f.write(f"""# Configuration file.

import arenas

# general -- first three parameters can be overwritten with command-line arguments (cf. "python tetracomposibot.py --help")

display_mode = 2
arena = {arena}
position = False 
max_iterations = 2001 #401*500

# affichage

display_welcome_message = False
verbose_minimal_progress = False # display iterations
display_robot_stats = False
display_team_stats = False
display_tournament_results = True
display_time_stats = False

# initialization : create and place robots at initial positions (returns a list containing the robots)

import robot_challenger
import robot_champion
import robot_genetic_training

def initialize_robots(arena_size=-1, particle_box=-1): # particle_box: size of the robot enclosed in a square
    global position
    #x_center = arena_size // 2 - particle_box / 2
    #y_center = arena_size // 2 - particle_box / 2
    x_init_pos = []
    if position == False:
        x_init_pos = [4,93]
        orientation_champion = 0
        orientation_challenger = 180
    else:
        x_init_pos = [93,4]
        orientation_champion = 180
        orientation_challenger = 0
    robots = {TheChosenOnes}
    return robots
""")

def getTeam(n, team):
    if team=="A":
        teamParam = [0, "orientation_champion", "A"]
    else:
        teamParam = [1, "orientation_challenger", "B"]
    behaviours = ["champion", "0", "1", "2", "3"]
    res = []
    for i in range(n):
        r=random.choice(behaviours)
        if r == "champion":
            res.append(f"""robot_champion.Robot_player(x_init_pos[{teamParam[0]}], arena_size//2-16+{i}*8, {teamParam[1]}, name="", team="{teamParam[2]}")""")
        else:
            res.append(f"""robot_challenger.Robot_player(x_init_pos[{teamParam[0]}], arena_size//2-16+{i}*8, {teamParam[1]}, name="", team="{teamParam[2]}, b="{r}")""")
    return res

def runIte(config):
    pproc = sp.Popen(["python3", "tetracomposibot.py", config], stdout=sp.PIPE)
    result = proc.communicate()[0].decode()

    return result.split("]")[0].split(' ')[-2], result.split("]")[1].split(' ')[-2]

def main():
    bestParamTrans = [0 for _ in range(17)]
    bestParamRot = [0 for _ in range(17)]
    gen=0

    childToTest = [(bestParamTrans, bestParamRot)]
    res = {}

    while gen<1000:
        arenaOrder = [random.randint(0, 5) for _ in range(10)]
        teamA = getTeam(3, "A")
        teamB = getTeam(4, "B")

        while childToTest!=[]:
            c = childToTest.pop()
            for a in arenaOrder:
                createConfig()
        """robot_challenger.Robot_player(x_init_pos[0], arena_size//2-16+i*8, orientation_champion, name="", team="A")"""
        """robot_champion.Robot_player(x_init_pos[1], arena_size//2-16+i*8, orientation_challenger, name="", team="B")"""
        gen+=1

if __name__=="__main__":
    main()
