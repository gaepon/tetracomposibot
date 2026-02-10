import subprocess as sp
import os
import random

def createConfig(TheChosenOnes, arena):
    with open("config_training.py", "w+") as f:
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
            res.append(f"""robot_challenger.Robot_player(x_init_pos[{teamParam[0]}], arena_size//2-16+{i}*8, {teamParam[1]}, name="", team="{teamParam[2]}", b="{r}")""")
    return res

def runIte(config):
    processus = "python3"
    if os.name == "nt":
        processus = "./.venv/Scripts/python.exe"
    proc = sp.Popen([processus, "tetracomposibot.py", config], stdout=sp.PIPE)
    result = proc.communicate()[0].decode()
    return int(result.split("]")[0].split(' ')[-2]), int(result.split("]")[1].split(' ')[-2])

def evolve(d):
    pass

def main():
    bestParamTrans = [0 for _ in range(17)]
    bestParamRot = [0 for _ in range(17)]
    gen=0

    childToTest = [(bestParamTrans, bestParamRot)]
    res = {}

    while gen<1:
        arenaOrder = [random.randint(0, 4) for _ in range(10)]
        teamA = getTeam(3, "A")
        teamB = getTeam(4, "B")

        while childToTest!=[]:
            c = childToTest.pop()
            teamA.append(f"""robot_genetic_training.Robot_player(x_init_pos[0], arena_size//2-16+3*8, orientation_champion, {c[0]}, {c[1]}, name="", team="A")""")
            teamA.extend(teamB)
            chosenOnes = "["+",".join(teamA)+"]"
            matchRes = []
            for a in arenaOrder:
                createConfig(chosenOnes, a)
                m=runIte("config_training")
                matchRes.append(m[0]-m[1])
            score=sum(matchRes)/len(matchRes)

            if len(res)<4:
                res[score]=c
            else:
                minScore = min(list(res.keys()))
                if score>minScore:
                    res.pop(minScore)
                    res[score]=c
        
        childToTest = evolve(res)

        gen+=1

        print(res)
    
if __name__=="__main__":
    main()
