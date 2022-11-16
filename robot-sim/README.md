Python Robotics Simulator
================================

This is a simple, portable robot simulator developed by [Student Robotics](https://studentrobotics.org).
Some of the arenas and the exercises have been modified for the Research Track I course

Installing and running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Pygame, unfortunately, can be tricky (though [not impossible](http://askubuntu.com/q/312767)) to install in virtual environments. If you are using `pip`, you might try `pip install hg+https://bitbucket.org/pygame/pygame`, or you could use your operating system's package manager. Windows users could use [Portable Python](http://portablepython.com/). PyPyBox2D and PyYAML are more forgiving, and should install just fine using `pip` or `easy_install`.

## Troubleshooting

When running `python run.py <file>`, you may be presented with an error: `ImportError: No module named 'robot'`. This may be due to a conflict between sr.tools and sr.robot. To resolve, symlink simulator/sr/robot to the location of sr.tools.

On Ubuntu, this can be accomplished by:
* Find the location of srtools: `pip show sr.tools`
* Get the location. In my case this was `/usr/local/lib/python2.7/dist-packages`
* Create symlink: `ln -s path/to/simulator/sr/robot /usr/local/lib/python2.7/dist-packages/sr/`

## Exercise
-----------------------------

To run one or more scripts in the simulator, use `run.py`, passing it the file names. 

I am proposing you three exercises, with an increasing level of difficulty.
The instruction for the three exercises can be found inside the .py files (exercise1.py, exercise2.py, exercise3.py).

When done, you can run the program with:

```bash
$ python run.py exercise1.py
```

You have also the solutions of the exercises (folder solutions)

```bash
$ python run.py solutions/exercise1_solution.py
```

Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```

[sr-api]: https://studentrobotics.org/docs/programming/sr/

How it works
------------

### General description ###
Our goal is to pair silver tokens with golden tokens. To do that we repeat some actions:
1) the robot are looking for a silver token that has not yet been identified
2) get closer to it and grab it
3) looking for a golden token that is not identified yet to pair it with and release the silver token
4) restart from 1. until the robot find new silver tokens

### A little bit more explained ###
In the following rows I'll explain which function deals with the parts just described.
1) the main function deals with the search for free silver tokens, that is made with several control to detect, turn and drive the robot to the closest token.
2) when the robot is close to a silver token and the robot should grab it, I call the function grab_token() that allows the robot to grab it.
3) the grab_token() function is build to check the free golden token and go close to it and release the silver token.

Also the find_token_silver() and find_token_gold() function check if the silver or golden token are just pair with another silver token, and if not compute the distance, the angle and the code of the token that the robot is whatching.


Pseudocode
----------
	a_th <- 2
	d_th <- 0.4
	dist <- float
	silver_code <- list
	golden_code <- list

	find_token_silver()
		dist <- 100
		for each token in R.see()
	    		if code of token silver is not in silver code list
				if distance of token is less than dist and the color of token is 'silver':
					dist <- distance of token
					rot_y <- angle of token
					s_code <- silver code
			
			
	    if dist is equal to 100
		return -1, -1, -1
	    else
	   	return dist, rot_y, s_code
	   	
	   	
	find_token_gold()
	
		dist <- 100
		for each token in R.see()
			if code of token gold is not in silver code list
				if distance of token is less than dist and color of token is 'gold'
					dist <- token.dist
					rot_y <- token.rot_y
					g_code <- token.info.code
			
		if dist is equal to 100
			return -1, -1, -1
		else:
		   	return dist, rot_y, g_code
	   	
	   	
	grab_token(code_silver:list)
	
		if I take the token
			add the silver code to list
			release <- True
			
			while release
				dist_gold, rot_gold, code_gold <- find_token_gold()
				if dist is equal to -1
					turn the robot
				else if dist_silver is less than d_th
					release the silver token
					make a step back with the robot
					add the golden token at his list
					release <- False
				else if the value of rot_gold is between -a_th and a_th
					the robot must go on
				else if rot_gold is less than -a_th
					turn left
				else if rot_gold is greater than a_th
					turn right
			
			
	main()
		
		while 1
		
			dist_silver, rot_silver, code_silver <- find_token_silver()
			
			if size of sivler code list is equal to 6 and the size of golden code list is equal to 6
				exit
			if dist_silver is equal to -1
				turn the robot
			else if dist_silver is less than d_th
				grab_token(code_silver)
			else if the value of rot_silver is between -a_th and a_th
				the robot must go on	
			else if rot_silver is less than -a_th
				turn left
			else if rot_silver is greater than a_th
				turn right
			
### Possible improvement ###
A possible improvement could be to optimize the search for the closest tokens, by having the robot do a mapping of the environment and update the position of the tokens when it moves
