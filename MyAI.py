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

class MyAI ( Agent ):

	def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
		self.x = 0
		self.y = 0 
		self.direction = 'right'
		self.hasArrow = True 
		self.hasGold = False
		self.wumpusDead = False 
		self._gameState = [[['@','v'],[],[],[]],[[],[],[],[]],[[],[],[],[]],[[],[],[],[]]]
		self.visited = []
		self.retrace = False 
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
	
		
	
	def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
		if(breeze): #retrace steps and climb out 
			self.retrace = True 
		if(scream): 
			self.wumpusDead = True 
		if(stench): #retrace steps and climb out 
			self.retrace = True 
		''' originally made the agent shoot and then move forward but average score is higher if agent climbs out when stench perceived
		if(stench and not breeze): 
			if(not self.wumpusDead and self.hasArrow): 
				return Agent.Action.SHOOT
			if(not self.wumpusDead and not self.hasArrow):
				self.x += 1
				return Agent.Action.FORWARD
			if(self.wumpusDead):
				self.x += 1
				return Agent.Action.FORWARD'''
		if(bump): #retrace steps and climb out  
			self.retrace = True
		if(glitter): #grab the gold and then retrace steps and climb out 
			self.retrace = True 
			return Agent.Action.GRAB
		if(self.retrace):
			if(self.x != 0):
				if(self.direction == 'right'):
					self.direction = 'up'
					return Agent.Action.TURN_LEFT
				if(self.direction == 'up'):
					self.direction = 'left'
					return Agent.Action.TURN_LEFT
				if(self.direction == 'left'):
					self.x -= 1
					return Agent.Action.FORWARD
			elif(self.x == 0 and self.y == 0):
				return Agent.Action.CLIMB
		else: #move forward if no percepts given  
			self.x += 1
			return Agent.Action.FORWARD
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================
	
    
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
