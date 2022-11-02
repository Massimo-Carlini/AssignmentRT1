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
   	return dist, rot_y, silver_code
   	
   	
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
   	return dist, rot_y, golden_code

def main():

	"""
	step = 0 is referred to silver token
	step = 1 is referred to golden token
	"""
	
	step = 0
	success_grab_silver = False
	success_release_silver = True
	timer = 30
	while(1):
		# token silver	
		if step == 0 and success_release_silver:
			print("0: sto guardando il token silver")
			# finche non ho preso un silver continuo a muovermi		
			while(not success_grab_silver):
				# cerco nella mappa il token argento e quando lo trovo mi ci dirigo
				if find_token_silver()[0] == -1 or find_token_silver()[1] == -1:
					turn(-10, 1)
				elif find_token_silver()[0] < d_th:
					success_grab_silver = R.grab()
					success_release_silver = False
					timer = 30
				elif find_token_silver()[1] > a_th:
					turn(1, 1)
				elif find_token_silver()[1] < -a_th:
					turn(-1, 1)
				elif -a_th < find_token_silver()[1] < a_th and find_token_silver()[0] > d_th:
					print("Ho trovato il token silver vicino")
					drive(30, 1)
					timer -= 1
					if timer == 0:
						turn(50,2)
						timer = 30
			# se prendo il token silver
			if(success_grab_silver):
				print("Ho preso il token silver")
				
				print(find_token_silver()[2])
				drive(30, 1)
				turn(10, 1)
				step = 1
				
		# token gold
		if step == 1 and success_grab_silver:
			print("1: sto guardando il token gold")
			# finche il token silver non viene rilasciato mi muovo verso il token gold		
			while(not success_release_silver):
				if find_token_gold()[0] == -1 or find_token_gold()[1] == -1:
					turn(-10, 1)
					print(step)
				elif find_token_gold()[0] < (d_th*(2)):
					print("Sono vicino al blocco gold, rilascio.")
					# lasciamo il blocco e ci giriamo per vedere gli altri blocchi
                    			success_release_silver = R.release() # now that is true and we exit from while loop
                    			drive(-12,1)
                    			turn(-30,2)
					print(find_token_gold()[2])
					step = 0
					timer = 30
				elif find_token_gold()[1] > a_th:
					turn(1, 1)
				elif find_token_gold()[1] < -a_th:
					turn(-1, 1)
				elif -a_th < find_token_gold()[1] < a_th and find_token_gold()[0] > d_th:
					drive(30, 1)
					timer -= 1
					if timer == 0:
						turn(10,2)
						timer = 30
			# se rilascio il token silver vicino al token gold torno alla ricerca di una altro token silver
			if(success_release_silver):
				print("Vado alla ricerca di un nuovo token silver")
				step = 0
				drive(30, 1)
				turn(10, 3)
		
main()
