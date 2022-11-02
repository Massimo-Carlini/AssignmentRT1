from __future__ import print_function

import time
from sr.robot import *

R = Robot()

a_th = 2
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

color_token = [MARKER_TOKEN_SILVER, MARKER_TOKEN_GOLD]

silver_code = []

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

def find_token():
    """
    Function to find the closest token

    Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
    	return -1, -1
    else:
        return dist, rot_y


def find_token_silver():
    """
    Function to find the closest silver token

    Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
    """
    dist=100
    for token in R.see():
	if token.dist < dist and token.info.marker_type == color_token[0]:
		dist = token.dist
		rot_y = token.rot_y
		color = token.info.marker_type
		
		
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y
   	
   	
def find_token_gold():
    """
    Function to find the closest golden token

    Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
    """
    dist=100
    for token in R.see():
	if token.dist < dist and token.info.marker_type == color_token[1]:
		dist = token.dist
		rot_y = token.rot_y
		color = token.info.marker_type
		golden_code = token.info.code
		
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y
   	
   	
def grab_token():
	if R.grab():
		print("Ho preso il blocco!")
		turn(30,1)	
		while R.release():
			dist_gold, rot_gold = find_token_gold()
			print("Cerco il token gold dove rilasciare il blocco")
			# if I am close enough to the gold token I can release the silver token
			if dist_gold < d_th:
				R.release()
				drive(-20,1)
				turn(-30,2)
			elif -a_th <= rot_gold <= a_th:
				print("Ah, that'll do. (golden)")
				drive(50,2)
			else:
				turn(10,1)
		
		
def change_a_bit(dist_silver, rot_silver):

	"""
		Function to align the robot to the token, in order to grab it well
	"""
	if (dist_silver < d_th):
		print("Found it!!")
		grab_token()
		
	elif -a_th <= rot_silver <= a_th: # if the robot is well aligned with the token, we go forward
		print("Ah, that'll do.")
		drive(30, 1)
		
	# with the following control, I make sure that the robot is well aligned with silver token
	elif rot_silver < -a_th: # left control
		print("Left a bit... silver")
		turn(-8, 1)
		
	elif rot_silver > a_th: # right control
		print("Right a bit... silver")
		turn(+8, 1)
		

def main():
	
	while 1:
	
		dist_silver, rot_silver = find_token_silver()
		dist_golden, rot_golden = find_token_gold()
		
		if (dist_silver > d_th) and (-a_th < rot_silver < a_th):
			print("Let's start!")
			drive(30,1)
		
		if (dist_silver < d_th) or (dist_silver == -1) or (rot_silver == -1):
			change_a_bit(dist_silver, rot_silver)
			

	
		
main()
