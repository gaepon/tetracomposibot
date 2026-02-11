# Configuration file.

#FILE AUTO-GENERATED DURING TRAINING BY geneticTrainer.py

import arenas

# general -- first three parameters can be overwritten with command-line arguments (cf. "python tetracomposibot.py --help")

display_mode = 2
arena = 3
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
    robots = [robot_challenger.Robot_player(x_init_pos[0], arena_size//2-16+0*8, orientation_champion, name="", team="A", b="1"),robot_champion.Robot_player(x_init_pos[0], arena_size//2-16+1*8, orientation_champion, name="", team="A"),robot_challenger.Robot_player(x_init_pos[0], arena_size//2-16+2*8, orientation_champion, name="", team="A", b="2"),robot_genetic_training.Robot_player(x_init_pos[0], arena_size//2-16+3*8, orientation_champion, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], name="", team="A"),robot_challenger.Robot_player(x_init_pos[1], arena_size//2-16+0*8, orientation_challenger, name="", team="B", b="3"),robot_champion.Robot_player(x_init_pos[1], arena_size//2-16+1*8, orientation_challenger, name="", team="B"),robot_challenger.Robot_player(x_init_pos[1], arena_size//2-16+2*8, orientation_challenger, name="", team="B", b="3"),robot_challenger.Robot_player(x_init_pos[1], arena_size//2-16+3*8, orientation_challenger, name="", team="B", b="0")]
    return robots
