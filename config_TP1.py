# Configuration file.

import arenas

# general -- first three parameters can be overwritten with command-line arguments (cf. "python tetracomposibot.py --help")

display_mode = 0
arena = 1
position = False 
max_iterations = 501 #401*500

# affichage

display_welcome_message = False
verbose_minimal_progress = True # display iterations
display_robot_stats = False
display_team_stats = False
display_tournament_results = False
display_time_stats = True

# initialization : create and place robots at initial positions (returns a list containing the robots)

import robot_dumb
import robot_braitenberg_avoider as RAvoid
import robot_braitenberg_loveWall as RWall
import robot_braitenberg_hateWall as RAWall
import robot_subsomption as RSub

def initialize_robots(arena_size=-1, particle_box=-1): # particle_box: size of the robot enclosed in a square
    #x_center = arena_size // 2 - particle_box / 2
    y_center = arena_size // 2 - particle_box / 2
    robots = []
    robots.append(RAvoid.Robot_player(4, y_center, 0, name="Sea Otter", team="The Otter Team"))
    #robots.append(RWall.Robot_player(6, y_center, 0, name="River Otter", team="The Otter Team"))
    robots.append(RAWall.Robot_player(8, y_center, 0, name="Otter Space", team="The Otter Team"))
    robots.append(RSub.Robot_player(6, y_center, 0, name="Smort Otter", team="The Otter Team"))
    return robots
