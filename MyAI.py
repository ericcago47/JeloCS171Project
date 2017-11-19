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
from random import choice 

class MyAI ( Agent ):

	def __init__ ( self ):
		# ======================================================================
		# YOUR CODE BEGINS
		# ======================================================================
		self.x = 1 
		self.y = 1 
		self.hasArrow = True 
		self.rowLen = None
		self.colLen = None
		self.wumpusDead = False 
		self.hasGold = False
		self.direction = 'Right'  
		self.gameNodes = {(1,1): [(2,1), (1,2)]} #graph holding visited nodes as keys and their neighboring nodes as values 
		self.gameStates = defaultdict(list) 
		self.gameStates[(1,1)].append('S') #graph holding nodes as keys and their threat state as values 
		self.moves = [] 
		self.inProgress = False 
		self.moveHistory = [] 	
		self.retrace = False 	
		self.iterate = False 	
		self.retraceStack = []
		pass
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
	def generateNeighbors(self, x:int, y:int): 
		neighbors = [] 
		if x >= 2:
			#print('Left nbr: ', x-1, ',', y)  
			neighbors.append((x-1, y)) #generate the left neighbor 
		if self.rowLen == None or self.x < self.rowLen: 
			#print('Right nbr: ', x+1, ',', y) 
			neighbors.append((x+1, y)) #generate the right neighbor
		if y >= 2:
			#print('Below nbr: ', x, ',', y-1)
			neighbors.append((x, y-1)) #generate the neighbor below
		if self.colLen == None or self.y < self.colLen: 
			#print('Above nbr: ',x, ',', y+1) 
			neighbors.append((x, y+1)) #generate the neighbor above
		#print('generateNeighbors() neighbors: ', neighbors) 
		return neighbors 

	def updateGameNodes(self):
		print('(x,y): (', self.x,self.y,')')
		print('GameNodes Dict: ', self.gameNodes) 
		if (self.x, self.y) not in self.gameNodes.keys():
			print('genNbrs: ', self.generateNeighbors(self.x,self.y)) 
			self.gameNodes[(self.x, self.y)] = self.generateNeighbors(self.x,self.y)
#			self.gameNodes[(self.x, self.y)].extend(generateNeighbors(self.x,self.y))

	def updatePossibleThreat(self, threat:str):
		'''Adds Possbles to neighboring nodes IFF they haven't been visited, it has not been labeled no threat, and it has not been labeled/marked already (avoid duplicates)'''
		for node in self.gameNodes[(self.x, self.y)]:
			if node not in self.gameNodes and ('N' + threat) not in self.gameStates[node] and ('P' + threat) not in self.gameStates[node]:  #check that the node isnt visited because that means it is safe  
				self.gameStates[node].append('P'+threat)  

	def noSameThreat(self, threat: str): 
		'''Checks if neighbors' states have same possible threat, and marks no threat if it doesnt'''
		for node in self.gameNodes[(self.x,self.y)]:
			if node in self.gameStates and ('P' + threat) not in self.gameStates[node]: #if neighbors haven't been marked with that possible threat, then we know for sure that no pit exists in that direction
				self.gameStates[node].append('N' + threat)


	def removeThreat(self, threat: str): #threat is OPPOSITE 
		'''If neighbor has a state, and that state is possible opposite threat, remove it and mark it NOT opposite threat. 
			Even if neighbor does not have a state, mark that it does not have an opposite threat. 
			If  neighbor has NP and NW mark it S'''
		neighbors = self.gameNodes[(self.x,self.y)] 
		for node in neighbors: 
			if node in self.gameStates.keys(): #check dictionary syntax --if node is a key in gameStates , if neighbor has a state 
				if ('P' + threat) in self.gameStates[node]:
					self.gameStates[node].remove('P'+threat) 
					self.gameStates[node].append('N' + threat)
					if threat == 'W':                
						if 'NP' in self.gameStates[node]: 
							self.gameStates[node] = ['S']
					elif 'NW' in self.gameState[node]: 
							self.gameStates[node] = ['S']
			else:	
				self.gameStates[node].append('N'+ threat) 
				
	def removePW(self): 
		'''If we kill the wumpus, removes all PW from the entire gameboard '''
		for node in self.gameNodes:
			if 'PW' in self.gameStates[node]: 
				self.gameStates[node].remove('PW') 

	def markSafe(self):
		'''if a square is safe AND HAS NO PERCEPTS , then all of its immediate (+-1)[so its not infinite] neighbors are safe (only called when stench AND breeze are false''' 
		if self.gameStates[(self.x,self.y)] == ['S']: 
			neighbors = self.generateNeighbors(self.x,self.y) 
			for node in neighbors: 
				self.gameStates[node] = ['S']
		
	def generateSafeMoves(self): 
		possibleMoves = self.gameNodes[(self.x, self.y)] #range 2-4
		result = []	
		for move in possibleMoves: 
			if move in self.gameStates.keys():
				if 'PP' not in self.gameStates[move] and 'PW' not in self.gameStates[move] and 'P' not in self.gameStates[move] and 'W' not in self.gameStates[move]: 
					result.append(move)
			else:
				result.append(move)
		print('Safe Moves: ', result) 	
		return result

		
	def findBestMove(self): #returns move with the highest evaluaton based on heuristic function (# turns/points lost) 
		safeMoves = self.generateSafeMoves()
		print('safeMoves: ', safeMoves) 
		if len(safeMoves) == 0: return 'climb'
		move = choice(safeMoves)  
		 	
		if self.x - move[0] == 1:
			return 'west'
		elif self.x - move[0] == -1: 
			return 'east'
		elif self.y-move[1] == 1: 
			 return 'south'
		elif self.y-move[1] == -1: 
			return 'north'	
		'''moveValues = {}
		if len(safeMoves) == 0: return 'climb'
		for move in safeMoves: 
			if self.x - move[0] == 1: moveValues['west'] = self.evaluateMoveWest() 
			elif self.x - move[0] ==  -1: moveValues['east'] = self.evaluateMoveEast()
			elif self.y - move[1] == 1: moveValues['south'] = self.evaluateMoveSouth() 
			elif self.y - move[1] == -1: moveValues['north'] = self.evaluateMoveNorth()
		print('moveValues in findBestMove: ', moveValues)  
		print('x,y in findBestMove: ', self.x, ',', self.y) 
		return max(moveValues, key = moveValues.get) 
		'''	
	def generateChosenStack(self,move): 
		if move == 'west': return self.generateWestMoveStack()
		elif move == 'east': return self.generateEastMoveStack() 
		elif move == 'south': return self.generateSouthMoveStack() 
		elif move == 'north': return self.generateNorthMoveStack()
		elif move == 'climb': return ['CLIMB']
				
	def generateEastMoveStack(self): 
		movesStack = []  
		if self.direction == 'Down': 
			movesStack.append('TURN_LEFT') 
		elif self.direction == 'Left':
			movesStack.append('TURN_RIGHT')
			movesStack.append('TURN_RIGHT')
		elif self.direction == 'Up': 
			movesStack.append('TURN_RIGHT')
		self.direction = 'Right'
		movesStack.append('FORWARD'); 
		return movesStack	
	
	def generateWestMoveStack(self):
		movesStack = [] 
		if self.direction == 'Down':
			movesStack.append('TURN_RIGHT')
		elif self.direction == 'Right':
			movesStack.append('TURN_RIGHT')
			movesStack.append('TURN_RIGHT')
		elif self.direction == 'Up':
			movesStack.append('TURN_LEFT')
		movesStack.append('FORWARD');
		self.direction = 'Left' 
		return movesStack 

	def generateNorthMoveStack(self): 
		movesStack = [] 
		if self.direction == 'Right':
			movesStack.append('TURN_LEFT')
		elif self.direction == 'Down':
			movesStack.append('TURN_RIGHT')
			movesStack.append('TURN_RIGHT')
		elif self.direction == 'Left':
			movesStack.append('TURN_RIGHT')
		movesStack.append('FORWARD');
		self.direction = 'Up' 
		return movesStack 

	def generateSouthMoveStack(self): 
		movesStack = [] 
		if self.direction == 'Left':
			movesStack.append('TURN_LEFT')
		elif self.direction == 'Up':
 			movesStack.append('TURN_RIGHT')
 			movesStack.append('TURN_RIGHT')
		elif self.direction == 'Right':
			movesStack.append('TURN_RIGHT')
		self.direction = 'Down'
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

	def updateCoordinates(self): 
		if self.direction == 'Right': self.x += 1
		elif self.direction == 'Left': self.x -= 1
		elif self.direction == 'Down': self.y -= 1
		elif self.direction == 'Up': self.y += 1		

	def backtrack(self):
		for move in range(len(self.moveHistory)): 
			lastMove = self.moveHistory[len(self.moveHistory)-1-move]
			if lastMove == 'TURN_LEFT': 
				self.moves.append('TURN_RIGHT')
			elif lastMove == 'TURN_RIGHT':
				self.moves.append('TURN_LEFT')
			elif lastMove == 'FORWARD': 
				self.moves.append('FORWARD')
		self.moves.append('CLIMB') 

	def getAction( self, stench, breeze, glitter, bump, scream ):
		# ======================================================================
		# YOUR CODE BEGINS
		# ======================================================================
		self.updateGameNodes() 
		if not stench and not breeze:
			self.markSafe()
		
		if glitter: 
			self.hasGold = True
			self.inProgress = True 
			self.moveHistory.pop() 	
			self.moves = ['TURN_LEFT', 'TURN_LEFT', 'FORWARD']
			self.backtrack() 	 
			return Agent.Action.GRAB

		if bump: 
			if self.direction == 'Right': 
				self.rowLen = self.x
				self.x -= 1
				for node in self.gameNodes: 
					if node[0] == self.x: 
						self.gameNodes[node].remove((node[0]+1,node[1]))
				self.gameNodes.pop((self.x+1,self.y))
			elif self.direction == 'Up': 
				self.colLen = self.y 
				self.y -= 1
				for node in sel.gameNodes:  
					if node[1] == self.y: 
						self.gameNodes[node].remove((node[0], node[1]+1)) #error list.remove(x) is not in the list 
				self.gameNodes.pop((self.x, self.y+1)) 
		if scream: 
			self.wumpusDead = True 
			self.removePW()

		if stench:
			if breeze and self.x == 1 and self.y == 1: 
				return Agent.Action.CLIMB		
			if not self.wumpusDead: 
				self.updatePossibleThreat('W')
			if not breeze: 
				self.removeThreat('P')
			if self.hasArrow and not self.inProgress:  
				self.hasArrow = False
				if self.direction == 'Right': 
					self.gameStates[(self.x+1, self.y)].remove('PW') 
				elif self.direction == 'Left': 
					self.gameStates[(self.x-1, self.y)].remove('PW') 
				elif self.direction == 'Up': 
					self.gameStates[(self.x,self.y+1)].remove('PW') 
				elif self.direction == 'Down': 
					self.gameStates[(self.x, self.y-1)].remove('PW') 
				return Agent.Action.SHOOT

		if breeze: 
			self.updatePossibleThreat('P') 
			if not stench: 
				self.removeThreat('W') 
		if not self.inProgress: 
			bestMove = self.findBestMove() 
			if bestMove == 'climb': return Agent.Action.CLIMB
			self.moves = self.generateChosenStack(bestMove)
			self.inProgress = True 

		if self.inProgress: 
			if self.hasGold and self.x == 1 and self.y == 1: 
				return Agent.Action.CLIMB
			print('self.moves: ', self.moves) 
			if len(self.moves) == 1: self.inProgress = False 
			move = self.moves.pop(0)
			self.moveHistory.append(move) 
			agentMove = 'Agent.Action' + '.' + move  
			print('STATES: ') 
			for nbr in self.gameNodes[(self.x,self.y)]:
				print(nbr[0],',',nbr[1],': ',self.gameStates[(nbr[0], nbr[1])])
			if move == 'FORWARD': 
				self.updateCoordinates() 
			print()
			print()
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
