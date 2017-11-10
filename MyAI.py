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
from collections import defaultdict 
import inspect 

class MyAI ( Agent ):

    def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
		self.x = 1 
		self.y = 1 
		self.hasArrow = False 
		self.rowLen 
		self.colLen 
		self.wumpusDead = False 
		self.hasGold = False 
		self.gameNodes = {(1,1): [(2,1), (1,2)]} #graph holding visited nodes as keys and their neighboring nodes as values 
		self.gameStates = defaultdict(list) 
		self.gameStates[(1,1)].append('S') #graph holding nodes as keys and their threat state as values 
		self.gameMoves = [] 
	
        pass
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
	def generateNeighbors(int x, int y): 
		neighbors = [] 
		if x >= 2 
			neighbors.append((x-1, y)) #generate the left neighbor 
        neighbors.append((x+1, y)) #generate the right neighbor
		if y >= 2
			neighbors.append((x, y-1)) #generate the meighbor below
		neighbors.append((x, y+1)) #generate the neighbor above
		return neighbors 

	def updateGameNodes():
		if (self.x, self.y) not in self.gameNodes: 
			self.gameNodes[(self.x, self.y)].append(generateNeighbors(self.x,self.y))

	def updatePossibleThreat(threat:str):
		#possiblePits = generateNeighbors(self.x,self.y) 
		for node in self.gameNodes[(self.x, self.y)]:
			if node not in self.gameNodes and ('N' + threat) not in self.gameStates[node]: : #check that the node isnt visited because that means it is safe  
				self.gameStates[node].append('P'+threat)  

	def notThreat(threat: str, stench: bool, breeze: bool):
		#implement inspect stuff 
		if breeze == False or stench == False:
			neighbors = generateNeighbors(self.x,self.y) 
			for node in neighbors: 
				if node in self.gameStates.keys(): #check dictionary syntax --if node is a key in gameStates  
					if ('P' + threat) in self.gameStates[node]:
						self.gameStates[node].remove('P'+threat) 
						self.gameStates[node].append('N' + threat)
						if threat == 'W':                
							if 'NP' in self.gameStates[node]: 
								self.gameStates[node] = ['S']
						elif 'NW' in self.gameState[node]: 
								self.gameStates[node] = ['S']

	def markSafe(): 
		if self.gameStates[(self.x,self.y)] == ['S']: 
			neighbors = generateNeighbors(self.x,self.y) 
			for node in neighbors: 
				self.gameStates[node] = ['S']
		
	def generateMoves(): 
		
				

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
         
        return Agent.Action.CLIMB
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================

    
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
