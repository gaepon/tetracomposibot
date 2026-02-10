# Configuration file.

#FILE AUTO-GENERATED DURING TRAINING BY geneticTrainer.py

import arenas

# general -- first three parameters can be overwritten with command-line arguments (cf. "python tetracomposibot.py --help")

display_mode = 2
arena = 0
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
    robots = [robot_champion.Robot_player(x_init_pos[0], arena_size//2-16+0*8, orientation_champion, name="", team="A"),robot_champion.Robot_player(x_init_pos[0], arena_size//2-16+1*8, orientation_champion, name="", team="A"),robot_champion.Robot_player(x_init_pos[0], arena_size//2-16+2*8, orientation_champion, name="", team="A"),robot_genetic_training.Robot_player(x_init_pos[0], arena_size//2-16+3*8, orientation_champion, [-0.580198763275847, 0.25874772651412625, -0.6164841220448951, -0.4879737489413136, -0.8709730101553856, -0.9666063355146794, -0.9627983194091307, 0.7923455919839042, 0, -0.10763792142529693, -0.0309890481392181, 0.14509538436022407, -0.408960943173015, 0.5391428852509859, 0.30821839601311884, -0.5668072782317113, 0.6104852662309987], [0.7321823107871384, -0.00122177691339731, 0.8354403611090027, -0.24436041612772175, 0.25436712659558913, -0.8417265807546479, -0.36999248427772025, 0.741279369757089, -0.1436705877086928, 0.0194832534960081, -0.25468251498857875, 0.16419383861169856, -0.6669472008854269, -0.9055169269862473, -0.09834206854672645, -0.9259759612293368, 0], name="", team="A"),robot_challenger.Robot_player(x_init_pos[1], arena_size//2-16+0*8, orientation_challenger, name="", team="B", b="0"),robot_challenger.Robot_player(x_init_pos[1], arena_size//2-16+1*8, orientation_challenger, name="", team="B", b="1"),robot_challenger.Robot_player(x_init_pos[1], arena_size//2-16+2*8, orientation_challenger, name="", team="B", b="1"),robot_champion.Robot_player(x_init_pos[1], arena_size//2-16+3*8, orientation_challenger, name="", team="B")]
    return robots
