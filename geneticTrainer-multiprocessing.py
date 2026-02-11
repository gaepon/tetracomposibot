import subprocess as sp
import os
import random
import copy
import multiprocessing
from multiprocessing.managers import DictProxy

##################################################################
## The Following Script Is There To Train The Genetic Algorirhm ##
##################################################################


def createConfig(TheChosenOnes:list, arena:int, file:str)->None:
    """
    Creates a config file that can be used by tetracomposibot.py
    
    :param TheChosenOnes: Robots used in the config
    :type TheChosenOnes: list
    :param arena: Arena to use in the config
    :type arena: int
    :param file: Filename for the created config
    :type file: str
    """
    with open(file+".py", "w+") as f:
        f.write(f"""# Configuration file.

#FILE AUTO-GENERATED DURING TRAINING BY geneticTrainer.py

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
display_team_stats = True
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

def getTeam(n:int, team:str)->list[str]:
    """
    Generates a team of n robots with random behaviours
    
    :param n: The number of robots to create
    :type n: int
    :param team: The team to which the robots will be affected
    :type team: str
    :return: A list containing preconfigured and positioned robots
    :rtype: list[str]
    """

    if team=="A":
        teamParam = [0, "orientation_champion", "A"]
    else:
        teamParam = [1, "orientation_challenger", "B"]

    behaviours = ["champion", "0", "1", "2", "3", "4"]

    res = []
    for i in range(n):
        r=random.choice(behaviours)
        if r == "champion":
            res.append(f"""robot_champion.Robot_player(x_init_pos[{teamParam[0]}], arena_size//2-16+{i}*8, {teamParam[1]}, name="", team="{teamParam[2]}")""")
        else:
            res.append(f"""robot_challenger.Robot_player(x_init_pos[{teamParam[0]}], arena_size//2-16+{i}*8, {teamParam[1]}, name="", team="{teamParam[2]}", b="{r}")""")
    return res

def runIte(config:str, procnum:int, returnDict:DictProxy)->None:
    """
    Runs a paintwars match with tetracomposibot
    
    :param config: The config file to use
    :type config: str
    :param procnum: The processus number
    :type procnum: int
    :param returnDict: A synced dictionary containing the paintwar's results
    :type returnDict: DictProxy
    """
    processus = "python3"

    #Windows being windows...
    if os.name == "nt":
        processus = "./.venv/Scripts/python.exe"

    proc = sp.Popen([processus, "tetracomposibot.py", config], stdout=sp.PIPE)

    #Get tetracomposibot's prints
    result = proc.communicate()[0].decode().split('\n')

    returnDict[procnum] = (int(result[-2].split("]")[0].split(' ')[-2]) - int(result[-2].split("]")[1].split(' ')[-2]), int(result[3].split()[-2]))

def mutate(genome:list[float], chance:float, sigma:float)->list[float]:
    """
    Docstring for mutate
    
    :param genome: Description
    :type genome: list[float]
    :param chance: Description
    :type chance: float
    :param sigma: Description
    :type sigma: float
    :return: Description
    :rtype: list[float]
    """

    for i in range(len(genome)):
        random.normalvariate
        if random.random()>=chance:
            genome[i]+=random.normalvariate(0, sigma)
            if random.random()<=0.05: #Catastrophic reroll
                genome[i]=random.uniform(-1, 1)
    return genome

def evolve(parents:dict):
    children = []

    if len(parents)>1:
        # 2 mutation behaviours, one to fine-tune, the other to get out of niches
        for k in parents.keys():
            p = copy.deepcopy(parents)
            children.append((mutate(p[k][0], 0.91, 0.09), mutate(p[k][1], 0.91, 0.09)))
            children.append((mutate(p[k][0], 0.75, 0.4), mutate(p[k][1], 0.75, 0.4)))
        
        #Setting up crossovers !

        listKeys = list(parents.keys())

        for _ in range(2):
            sP1 = max(listKeys)
            listKeys.remove(sP1)
            p1 = parents[sP1]
            sP2 = random.choice(listKeys)
            listKeys.remove(sP2)
            p2 = parents[sP2]

            tr=[]
            ro=[]

            lCrossParent = [p1, p2]
            k=0

            for i in range(len(p1[0])):
                if random.random()>0.98:
                    k+=1
                tr.append(lCrossParent[k%2][0][i])
            for i in range(len(p1[1])):
                if random.random()>0.98:
                    k+=1
                ro.append(lCrossParent[k%2][1][i])
            
            children.append((copy.copy(tr), copy.copy(ro)))
    else:
        for i in range(5):
            p = copy.deepcopy(parents)
            k = list(p.keys())[0]
            children.append((mutate(p[k][0], 0.91, 0.09), mutate(p[k][1], 0.91, 0.09)))
            children.append((mutate(p[k][0], 0.75, 0.4), mutate(p[k][1], 0.75, 0.4)))

    return children

def run(TheChosenOnes, arena, config, procnum, returnDict):
    file = config+f"_{procnum}"
    createConfig(TheChosenOnes, arena, file)
    runIte(file, procnum, returnDict)

def main():
    bestParamTrans = [0 for _ in range(17)]
    bestParamRot = [0 for _ in range(17)]
    gen=0

    childToTest = [(bestParamTrans, bestParamRot)]
    res = {}
    bestEver = None
    bestGen = 0

    manager = multiprocessing.Manager()
    returnDict = manager.dict()

    while gen<250:
        if gen%5==0:
            print("Génération", gen, "en cours d'entrainement")
        arenaOrder = [random.randint(0, 4) for _ in range(6)]
        teamA = getTeam(3, "A")
        teamB = getTeam(4, "B")

        while childToTest!=[]:
            robots=[]
            c = childToTest.pop()
            robots.extend(teamA)
            robots.append(f"""robot_genetic_training.Robot_player(x_init_pos[0], arena_size//2-16+3*8, orientation_champion, {c[0]}, {c[1]}, name="", team="A")""")
            robots.extend(teamB)
            chosenOnes = "["+",".join(robots)+"]"
            jobs = []


            for i in range(len(arenaOrder)):
                a = arenaOrder[i]
                p=multiprocessing.Process(target=run, args=(chosenOnes, a, "config_training", i, returnDict))
                jobs.append(p)
                p.start()
            
            for proc in jobs:
                proc.join()

            su=0
            score=0
            for _, v in returnDict.items():
                score+=v[0]
                su+=v[1]
            score=score/len(returnDict.keys())+su/len(returnDict.keys())

            if len(res)<4:
                res[score]=c
            else:
                minScore = min(list(res.keys()))
                if score>minScore:
                    res.pop(minScore)
                    res[score]=c
            
            if bestEver is None:
                bestEver=(score, c)
                bestGen=gen
            elif bestEver[0]<score:
                bestEver=(score, c)
                bestGen=gen
        
        childToTest = evolve(res)

        gen+=1

    print(res)
    print(f"Best Ever Performing Little Fella : {bestEver[1]} with a score of {bestEver[0]} from generation {bestGen}")
    
if __name__=="__main__":
    main()
