# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent
import random

class MyAI ( Agent ):

    def __init__ ( self ):
	    # ======================================================================
	    # YOUR CODE BEGINS
	    # ======================================================================
	        
        self._direction = 'right'
		self._currentLocation = (0,0)
		self._X = 0
		self._Y = 0
		self._prevAction = None
		self._hasArrow = True
		self._hasGold = False
		self._rowLen = None
		self._colLen = None
		self._deadWumpus = False
		# Game state has min 4x4
		self._gameState = [[['@','v'],[],[],[]],[[],[],[],[]],[[],[],[],[]],[[],[],[],[]]]	
		# @ = Agent
		# v = Visited
		# br = Breeze
		# bu = Bump
		# s = Stench
		# p = Pit
		# go = Gold
		# gl = Glitter
		# w = Wumpus
		# pp = Possible Pit
		# pw = Possible Wumpus

        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
		nextMove = Agent.Action.CLIMB
		validMoves = __actions
		# random.randrange ( len ( self.__actions )
		# Updating GameState based on percepts
		if stench:
		    if 's' not in self._gameState[self._X][self._Y]:
		    	self._gameState[self._X][self._Y].append('s')		
		    	possibleThreat(self,'w')
		if breeze:
		    if 'br' not in self._gameState[self._X][self._Y]:
				self._gameState[self._X][self._Y].append('br')
				possibleThreat(self,'p')
			if self._currentLocation == (0,0):
				#TODO: Change in future; right now, climb out automatically
				nextMove = Agent.Action.CLIMB 
				self._prevAction = nextMove
				return nextMove
		if glitter:
			if 'gl' not in self._gameState[self._X][self._Y]:
				self._gameState[self._X][self._Y].append('gl')
	    	self._hasGold = True		
		   	nextMove = Agent.Action.GRAB
		    self._prevAction = nextMove
		    return nextMove
		if bump:
		    #update rowLen or cowLen here
		    if self._direction == 'right':
				self._colLen = self._Y + 1
		    elif self._direction == 'up':
				self._rowLen = self._X + 1
		if scream:
		    self._deadWumpus = True
		else:
		    pass
	   	    #randomly choose direction
		#if we know we're in first row, we know not to turn right

		if nextMove == Agent.Action.SHOOT:
		    self._hasArrow = False

		self._prevAction = nextMove
	        return nextMove
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    
    # ======================================================================
    # YOUR CODE BEGINS
    __actions = [
        Agent.Action.TURN_LEFT,
        Agent.Action.TURN_RIGHT,
        Agent.Action.FORWARD,
        Agent.Action.CLIMB,
        Agent.Action.SHOOT,
        Agent.Action.GRAB
    ]
    def validActions(self):
        pass

    def possibleThreat(self,threat_type):
	# Check past move / if square has been visited
	threat = 'p' + threat_type
	if pw == True:
            if self._X != (self._rowLen - 1) and ('v' not in self._gameState[self._X+1][self._Y]):
		#TODO: if row's not in gameState, add it! Same w/ columns
		if len(self._gameState) == (self._X + 1):
		    self._gameState.append([[],[],[],[]]) #TODO: Change this
		self._gameState[self._X+1][self._Y].append(threat)
	    if self._Y != (self._colLen - 1) and ('v' not in self._gameState[self._X][self._Y + 1]):            
	        if len(self._gameState[self._X]) == (self._Y + 1):
		    self._gameState[self._X].append([])
		self._gameState[self._X][self._Y+1].append(threat)
	    if self._X != 0 and ('v' not in self._gameState[self._X-1][self._Y]):
		self._gameState[self._X-1][self._Y].append(threat)
	    if self._Y != 0 and ('v' not in self._gameState[self._X][self._Y-1]):
		self._gameState[self._X][self._Y-1].append(threat)
	  		 
    # ======================================================================

    
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
