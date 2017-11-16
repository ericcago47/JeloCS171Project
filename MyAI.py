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
		self.rowLen = 4 
		self.colLen = 4
		self.wumpusDead = False 
		self.hasGold = False
		self.direction = 'Right'  
		self.gameNodes = {(1,1): [(2,1), (1,2)]} #graph holding visited nodes as keys and their neighboring nodes as values 
		self.gameStates = defaultdict(list) 
		self.gameStates[(1,1)].append('S') #graph holding nodes as keys and their threat state as values 
		self.moves = [] 
		self.inProgress = False 
		self.moveHistory = [] 	

		pass
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
	def generateNeighbors(self, x:int, y:int): 
		neighbors = [] 
		if x >= 2: 
			neighbors.append((x-1, y)) #generate the left neighbor 
		neighbors.append((x+1, y)) #generate the right neighbor
		if y >= 2:
			neighbors.append((x, y-1)) #generate the meighbor below
		neighbors.append((x, y+1)) #generate the neighbor above
		return neighbors 

	def updateGameNodes(self):
		if (self.x, self.y) not in self.gameNodes: 
			self.gameNodes[(self.x, self.y)].append(generateNeighbors(self.x,self.y))

	def updatePossibleThreat(self, threat:str):
		#possiblePits = generateNeighbors(self.x,self.y) 
		for node in self.gameNodes[(self.x, self.y)]:
			if node not in self.gameNodes and ('N' + threat) not in self.gameStates[node]:  #check that the node isnt visited because that means it is safe  
				self.gameStates[node].append('P'+threat)  

	def removeThreat(self, threat: str, stench: bool, breeze: bool):
		#implement inspect stuff 
		if breeze == False or stench == False:
			neighbors = self.gameNodes[(self.x,self.y)] 
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

	def markSafe(self): #if a square is safe AND HAS NO PERCEPTS , then all of its immediate (+-1)[so its not infinite] neighbors are safe 
	#need to reconsider this axiom and when how to represent that it has no percepts  ------> called in getAction if stench and breeze are false  
		if self.gameStates[(self.x,self.y)] == ['S']: 
			neighbors = self.generateNeighbors(self.x,self.y) 
			for node in neighbors: 
				self.gameStates[node] = ['S']
		
	def generateSafeMoves(self): 
		possibleMoves = self.gameNodes[(self.x, self.y)] #range 2-4
		result = []	
		for move in possibleMoves: 
			if move in self.gameStates.keys():
				if 'PP' not in self.gameStates[move]: 
					result.append(move)	
			else:
				result.append(move)
			
		return result

		
	def findBestMove(self): #returns move with the highest evaluaton based on heuristic function (# turns/points lost) 
		safeMoves = self.generateSafeMoves()
		moveValues = {}
		if len(safeMoves) == 0: return 'climb'
		for move in safeMoves: 
			if self.x - move[0] == 1: moveValues['west'] = self.evaluateMoveWest() 
			elif self.x - move[0] ==  -1: moveValues['east'] = self.evaluateMoveEast()
			elif self.y - move[1] == 1: moveValues['south'] = self.evaluateMoveSouth() 
			elif self.y - move[1] == -1: moveValues['north'] = self.evaluateMoveNorth() 
		return max(moveValues, key = moveValues.get) 
	
	def generateChosenStack(self,move): 
		if move == 'west': return self.generateWestMoveStack()
		elif move == 'east': return self.generateEastMoveStack() 
		elif move == 'south': return self.generateSouthMoveStack() 
		elif move == 'north': return self.generateNorthMoveStack()
		 
		elif move == 'climb': return ['CLIMB']
				
	def generateEastMoveStack(self): 
		movesStack = []  
		if self.direction == 'Down': 
			movesStack.append('TURN LEFT') 
		elif self.direction == 'Left': 
			movesStack.append('TURN RIGHT')
			movesStack.append('TURN RIGHT')
		elif self.direction == 'Up': 
			movesStack.append('TURN RIGHT')
		movesStack.append('FORWARD'); 
		return movesStack	
	
	def generateWestMoveStack(self):
		movesStack = [] 
		if self.direction == 'Down':
			movesStack.append('TURN RIGHT')
		elif self.direction == 'Right':
			movesStack.append('TURN RIGHT')
			movesStack.append('TURN RIGHT')
		elif self.direction == 'Up':
			movesStack.append('TURN LEFT')
		movesStack.append('FORWARD');
		return movesStack 

	def generateNorthMoveStack(self): 
		movesStack = [] 
		if self.direction == 'Right':
			movesStack.append('TURN LEFT')
		elif self.direction == 'Down':
			movesStack.append('TURN RIGHT')
			movesStack.append('TURN RIGHT')
		elif self.direction == 'Left':
			movesStack.append('TURN RIGHT')
		movesStack.append('FORWARD');
		return movesStack 

	
	def generateSouthMoveStack(self): 
		movesStack = [] 
		if self.direction == 'Left':
			movesStack.append('TURN LEFT')
		elif self.direction == 'Up':
 			movesStack.append('TURN RIGHT')
 			movesStack.append('TURN RIGHT')
		elif self.direction == 'Right':
			movesStack.append('TURN RIGHT')
		movesStack.append('FORWARD');
		return movesStack

	def evaluateMoveEast(self): 
		if self.direction == 'Right': return -1 
		elif self.direction == 'Left': return -3 
		elif self.direction == 'Up': return -2 
		elif self.direction == 'Down': return -2 

	def evaluateMoveNorth(self): 
		if self.direction == 'Right': return -2 
		elif self.direction == 'Left': return -2
		elif self.direction == 'Up': return -1	
		elif self.direction == 'Down': return -3 
	
	def evaluateMoveWest(self): 
		if self.direction == 'Right': return -3 
		elif self.direction == 'Left': return -1 
		elif self.direction == 'Down': return -2 
		elif self.direction == 'Up': return -2 
	
	def evaluateMoveSouth(self): 
		if self.direction == 'Right': return -2 
		elif self.direction == 'Left': return -2 
		elif self.direction == 'Up': return -3 
		elif self.direction == 'Down': return -1
		
				

	def getAction( self, stench, breeze, glitter, bump, scream ):
		# ======================================================================
		# YOUR CODE BEGINS
		# ======================================================================
		self.updateGameNodes() 
		self.removeThreat()	
		if not stench and not breeze:
			self.markSafe()
		
		if glitter: 
			self.hasGold = True
			return Agent.Action.GRAB

		if bump: 
			if self.direction == 'Right': self.rowLen = self.x
			elif self.direction == 'Up': self.colLen = self.y 

		if scream: 
			self.wumpusDead = True 

		if stench: 
			self.updatePossibleThreat('W')
			if not breeze: 
				self.markNotThreat('P', 
		if breeze: 
			self.updatePossibleThreat('P') 
			if not stench: 
				self.markNotThread('W' 
		if not self.inProgress: 
			bestMove = self.findBestMove() 
			if bestMove == 'climb': return Agent.Action.CLIMB
			self.moves = self.generateChosenStack(bestMove)
			self.inProgress = True 

		if self.inProgress: 
			if len(self.moves) == 1: self.inProgress = False 
			move = self.moves.pop()
			self.moveHistory.append(move) 
			agentMove = 'Agent.Action' + '.' + move  
			return eval(agentMove) 
			
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
