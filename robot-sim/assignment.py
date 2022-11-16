from __future__ import print_function

import time
from sr.robot import *


"""
	This algorithm allows the robot to take, move and pair silver tokens with gold ones
"""

R = Robot()

a_th = 2
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

color_token = [MARKER_TOKEN_SILVER, MARKER_TOKEN_GOLD]

# list of silver tokens that have already been paired with a gold token
silver_code = []

# list of golden tokens that are matched
golden_code = []


def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def find_token_silver():
    """
    Function to find the closest silver token

    Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
	s_code (float): code of the silver token identified
    """
    dist=100
    for token in R.see():
    	if token.info.code not in silver_code:
		if token.dist < dist and token.info.marker_type == color_token[0]:
			dist = token.dist
			rot_y = token.rot_y
			s_code = token.info.code
		
		
    if dist==100:
	return -1, -1, -1
    else:
   	return dist, rot_y, s_code
   	
   	
def find_token_gold():
    """
    Function to find the closest golden token

    Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
	g_code (float): code of the golden token identified
    """
    dist=100
    for token in R.see():
	if token.info.code not in golden_code:
		if token.dist < dist and token.info.marker_type == color_token[1]:
			dist = token.dist
			rot_y = token.rot_y
			g_code = token.info.code
		
    if dist==100:
	return -1, -1, -1
    else:
   	return dist, rot_y, g_code
   	
   	
def grab_token(code_silver):
	"""
		Function to grab the silver token and then release it if we are close to golden token
	"""
	if R.grab():
		silver_code.append(code_silver)
		print("Got it!")
		release = True
		
		while release:
			dist_gold, rot_gold, code_gold = find_token_gold()
			# if no token has been identified, we turn the robot
			if dist_gold == -1:
				turn(15, 0.5)
			# if I am close enough to the gold token I can release the silver token
			elif dist_gold < (d_th*1.6):
				R.release() 
				drive(-22,0.5)
				golden_code.append(code_gold)
				release = False
			# if the robot is well aligned with token, we go on
			elif -a_th <= rot_gold <= a_th:
				print("Ah, that'll do!")
				drive(40,0.5)
			# if the robot is not well aligned with token, we turn a bit on right or left side
			elif rot_gold < -a_th: # left control
				print("Left a bit...")
				turn(-1,1)
				
			elif rot_gold > a_th: # right control
				print("Left a bit...")
				turn(+1,1)
		
		
def main():
	
	while 1:
	
		dist_silver, rot_silver, code_silver = find_token_silver()
		
		if (len(silver_code) == 6) and (len(golden_code) == 6):
			print("That's all falks!")
			exit()
		# if no token has been identified, we turn the robot
		if dist_silver == -1:
			print("im in search of silver token")
			turn(15,0.5)
		# if I am close enough to the silver token I can grab it
		elif dist_silver < d_th:
			print("Silver token found!")
			grab_token(code_silver)
		# if the robot is well aligned with token, we go on	
		elif -a_th < rot_silver < a_th:
			print("Go!!")
			drive(40, 0.5)
		# if the robot is not well aligned with token, we turn a bit on right or left side	
		elif rot_silver < -a_th: # left control
			print("Left a bit... silver")
			turn(-1, 1)
			
		elif rot_silver > a_th: # right control
			print("Right a bit... silver")
			turn(+1, 1)
		

	
		
main()
