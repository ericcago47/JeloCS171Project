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
from math import sqrt

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
		self.numVisitedNodes = len(self.gameNodes) 
		self.score = 0
		self.safeNodes = defaultdict(list) 
		self.visitedNodes = []
		self.path = []
		self.homeSequence = [] 
		self.onWayHome = False 	
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
	def generateNeighbors(self, x:int, y:int): 
		neighbors = [] 
		if x >= 2:
			neighbors.append((x-1, y)) #generate the left neighbor 
		if self.rowLen == None:
			neighbors.append((x+1, y)) #generate the right neighbor
		elif self.x < self.rowLen: 
			neighbors.append((x+1, y)) #generate the right neighbor
		if y >= 2:
			neighbors.append((x, y-1)) #generate the neighbor below
		if self.colLen == None:
			neighbors.append((x, y+1)) #generate the neighbor above
		elif self.y < self.colLen:
			neighbors.append((x, y+1)) #generate the neighbor above
		return neighbors 

	def updateGameNodes(self):
		if (self.x, self.y) not in self.gameNodes.keys():
			self.gameNodes[(self.x, self.y)] = self.generateNeighbors(self.x,self.y)

	def markVisitedAsSafe(self):
		self.gameStates[(self.x,self.y)] = ['S']
			
	def updatePossibleThreat(self, threat:str):
		'''Adds Possibles to neighboring nodes IFF they haven't been visited, it has not been labeled no threat, and it has not been labeled/marked already (avoid duplicates)'''
		for node in self.gameNodes[(self.x, self.y)]:
			if node not in self.gameNodes and ('N' + threat) not in self.gameStates[node] and ('P' + threat) not in self.gameStates[node] and 'S' not in self.gameStates[node]:  #check that the node isnt visited because that means it is safe  
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
			if ('N' + threat) not in self.gameStates[node]: self.gameStates[node].append('N' + threat) 
			if node in self.gameStates.keys(): #check dictionary syntax --if node is a key in gameStates , if neighbor has a state 
				if ('P' + threat) in self.gameStates[node]:
					self.gameStates[node].remove('P'+threat) 
					if threat == 'W':                
						if 'NP' in self.gameStates[node]: 
							self.gameStates[node] = ['S']
					elif 'NW' in self.gameStates[node]: 
							self.gameStates[node] = ['S']
				
	def removePW(self): 
		'''If we kill the wumpus, removes all PW from the entire gameboard '''
		for node in self.gameStates: 
			if 'PW' in self.gameStates[node]: 
				self.gameStates[node].remove('PW')
				self.gameStates[node].append('NW') 

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
				#if 'S' in self.gameStates[move]: 
					result.append(move)
			else:
				result.append(move)
		return result

	def findBestMove(self): #returns move with the highest evaluaton based on heuristic function (# turns/points lost) 
		safeMoves = self.generateSafeMoves()
		if len(safeMoves) == 0: return 'climb'
		unvisitedNodes = [] 
		for move in safeMoves: 
			if move not in self.gameNodes: 
				unvisitedNodes.append(move) 
		if len(unvisitedNodes) != 0: 
			move = choice(unvisitedNodes) 
		else: move = choice(safeMoves)  
		#print('unvisited Moves: ', unvisitedNodes) 
		#print('chosen move: ', move) 	
		if self.x - move[0] == 1:
			return 'west'
		elif self.x - move[0] == -1: 
			return 'east'
		elif self.y-move[1] == 1: 
			 return 'south'
		elif self.y-move[1] == -1: 
			return 'north'	

	def generateChosenStack(self,move, givenDir): 
		if move == 'west': return self.generateWestMoveStack(givenDir)
		elif move == 'east': return self.generateEastMoveStack(givenDir) 
		elif move == 'south': return self.generateSouthMoveStack(givenDir) 
		elif move == 'north': return self.generateNorthMoveStack(givenDir)
		elif move == 'climb': return ['CLIMB']
		elif move == None: return []
				
	def generateEastMoveStack(self, givenDir): 
		movesStack = []  
		if givenDir == 'Down': 
			movesStack.append('TURN_LEFT') 
		elif givenDir == 'Left':
			movesStack.append('TURN_RIGHT')
			movesStack.append('TURN_RIGHT')
		elif givenDir == 'Up': 
			movesStack.append('TURN_RIGHT')
		movesStack.append('FORWARD'); 
		return movesStack	
	
	def generateWestMoveStack(self, givenDir):
		movesStack = [] 
		if givenDir == 'Down':
			movesStack.append('TURN_RIGHT')
		elif givenDir == 'Right':
			movesStack.append('TURN_RIGHT')
			movesStack.append('TURN_RIGHT')
		elif givenDir == 'Up':
			movesStack.append('TURN_LEFT')
		movesStack.append('FORWARD');
		return movesStack 

	def generateNorthMoveStack(self, givenDir): 
		movesStack = [] 
		if givenDir == 'Right':
			movesStack.append('TURN_LEFT')
		elif givenDir == 'Down':
			movesStack.append('TURN_RIGHT')
			movesStack.append('TURN_RIGHT')
		elif givenDir == 'Left':
			movesStack.append('TURN_RIGHT')
		movesStack.append('FORWARD');
		return movesStack 

	def generateSouthMoveStack(self, givenDir): 
		movesStack = [] 
		if givenDir == 'Left':
			movesStack.append('TURN_LEFT')
		elif givenDir == 'Up':
 			movesStack.append('TURN_RIGHT')
 			movesStack.append('TURN_RIGHT')
		elif givenDir == 'Right':
			movesStack.append('TURN_RIGHT')
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
		self.retrace = True 
		for move in range(len(self.moveHistory)): 
			lastMove = self.moveHistory[len(self.moveHistory)-1-move]
			if lastMove == 'TURN_LEFT': 
				self.moves.append('TURN_RIGHT')
			elif lastMove == 'TURN_RIGHT':
				self.moves.append('TURN_LEFT')
			elif lastMove == 'FORWARD': 
				self.moves.append('FORWARD')
		self.moves.append('CLIMB')
	
	def changeDirection(self, move): 
		if self.direction == 'Right': 
			if move == 'TURN_LEFT': 
				self.direction = 'Up'
			elif move == 'TURN_RIGHT': 	
				self.direction = 'Down'
		elif self.direction == 'Left': 
			if move == 'TURN_LEFT': 
				self.direction = 'Down'
			elif move == 'TURN_RIGHT': 
				self.direction = 'Up'
		elif self.direction == 'Down': 
			if move == 'TURN_LEFT':
				self.direction = 'Right'
			elif move == 'TURN_RIGHT': 
				self.direction = 'Left'
		elif self.direction == 'Up':
			if move == 'TURN_LEFT': 
				self.direction = 'Left'
			elif move == 'TURN_RIGHT':
				self.direction = 'Right'

	def changeTempDir(self, curDir, move): 
		if move == None: 
			return curDir 
		elif curDir == 'Right':
			if move == 'TURN_LEFT':
				return 'Up'
			elif move == 'TURN_RIGHT':
				return 'Down'
		elif curDir == 'Left':
			if move == 'TURN_LEFT':
				return 'Down'
			elif move == 'TURN_RIGHT':
				return 'Up'
		elif curDir == 'Down':
			if move == 'TURN_LEFT':
				return 'Right'
			elif move == 'TURN_RIGHT':
				return  'Left'
		elif curDir == 'Up':
			if move == 'TURN_LEFT':
				return 'Left'
			elif move == 'TURN_RIGHT':
				return 'Right'


	def getSafeNodes(self):
		for nbr in self.gameNodes:
			if 'S' in self.gameStates[nbr]: 
				for n in self.gameNodes[nbr]:
					if n in self.gameNodes: 
						self.safeNodes[nbr].append(n)

	def calcDist(self, otherX, otherY): 
		return sqrt((otherX-1)**2 + (otherY-1)**2) 
		 
	def findClosestHomeNbr(self, tempX, tempY): 
		nbrDist = {}
		currNbrs = self.safeNodes[(tempX,tempY)]
		self.visitedNodes.append((tempX,tempY))
		for nbr in currNbrs: 
			if nbr not in self.visitedNodes: 
				nbrDist[nbr] = self.calcDist(nbr[0],nbr[1])
		if len(nbrDist.keys()) == 0:
			firstPop = self.path.pop()
			return firstPop
		else:
			minNbr = min(nbrDist, key = nbrDist.get)
			self.path.append((tempX,tempY)) 
			return minNbr 

	def startSearchHome(self): 
		nextCoord = self.findClosestHomeNbr(self.x,self.y)
		print('next Coord', nextCoord) 
		while (nextCoord != (1,1)):  
			x = self.findClosestHomeNbr(nextCoord[0], nextCoord[1])
			nextCoord = x

	def executePath(self):
		finalList = []
		nextDir = None 
		print('first pop', self.path.pop(0))
		self.path.append((1,1)) 
		print('path ',self.path)
		c = ((self.x,self.y))
		cDir = self.direction 
		print('cXY: ', c) 
		print('cDir', cDir)
		#while len(self.path) != 0:
		while c!= (1,1) :
			for nextCoord in self.path:
				print('c is: ',c)
				print('nextCoord is: ', nextCoord) 
				if c[0] - nextCoord[0] == 1: 
					nextDir = 'west' 
				elif c[0] - nextCoord[0] == -1: 
					nextDir = 'east' 
				elif c[1] - nextCoord[1] == 1: 
					nextDir = 'south'
				elif c[1] - nextCoord[1] == -1:
					nextDir = 'north'
				elif nextCoord == (1,1):
					nextDir = 'climb'
				print('nextDir is: ', nextDir)
				c = nextCoord   
				tempStack = self.generateChosenStack(nextDir, cDir) 
				print('tempStack: ', tempStack)
				for move in tempStack: 	
					print(cDir, nextDir)
					x = self.changeTempDir(cDir, move)
					
					if x != None:cDir = x 
					print('inside tempStack: ', cDir) 
				
				finalList.extend(tempStack)
		print(finalList) 
		return finalList 
	
	def getAction( self, stench, breeze, glitter, bump, scream ):
		# ======================================================================
		# YOUR CODE BEGINS
		# ======================================================================
		#print('Score: ',self.score)
		self.updateGameNodes() 
		self.markVisitedAsSafe() 
		if self.score < -125 and self.retrace == False and self.inProgress == False:
			#print('score less than <-125, turning on self.retrace')
			self.visitedNodes.append((self.x,self.y))
			self.path.append((self.x,self.y)) 
			self.getSafeNodes()
			self.retrace = True

		if self.retrace and not self.onWayHome:
			if self.x == 1 and self.y == 1: 
				self.score -=1 
				return Agent.Action.CLIMB 
			#print('initializing homeSequence') 
#			self.homeSequence = self.startSearchHome()
			self.startSearchHome()
			self.homeSequence = self.executePath() 
			print('HOMSEQ: ', self.homeSequence)
			self.onWayHome = True 

		if self.retrace and self.onWayHome: 
			if self.x == 1 and self. y == 1: 
				self.score -= 1
				return Agent.Action.CLIMB
			print(self.x, self.y) 
			
			#if len(self.homeSequence) == 1: 
			#	self.onWayHome = False
			
			nextMove = self.homeSequence.pop(0)
			print('in getAction: ', nextMove) 
			#print('next move home: ', nextMove)  
			agentMove = 'Agent.Action' + '.' + nextMove 
			if nextMove == 'FORWARD': 
				self.updateCoordinates()
			self.changeDirection(nextMove)
			self.score -= 1
			return eval(agentMove) 
		
		if not stench and not breeze:
			#print('Calling self.markSafe()')
			self.markSafe()
		
		if glitter and self.retrace == False: 
			#print('Picking up glitter')
			self.hasGold = True
			self.inProgress = False 
			#self.inProgress = True 
			self.moveHistory.pop() 	
			#self.moves = ['TURN_LEFT', 'TURN_LEFT', 'FORWARD']
			#self.backtrack() 	 
			self.score -= 1
			self.retrace = True 
			self.visitedNodes.append((self.x,self.y))
			self.path.append((self.x,self.y))
			self.getSafeNodes()
			return Agent.Action.GRAB
		
		if bump:
		#	print('Just bumped')
			self.moveHistory.pop() 
			if self.direction == 'Right': 
				self.x -= 1
				self.rowLen = self.x
				for node in self.gameNodes: 
					if node[0] == self.x: 
						self.gameNodes[node].remove((node[0]+1,node[1]))
				self.gameNodes.pop((self.x+1, self.y))
			elif self.direction == 'Up': 
				self.y -= 1
				self.colLen = self.y 
				for node in self.gameNodes:  
					if node[1] == self.y: 
						self.gameNodes[node].remove((node[0], node[1]+1)) #error list.remove(x) is not in the list 
				self.gameNodes.pop((self.x, self.y+1))
		#	print('End of bump if statement') 

		if scream: 
			#print('Just screamed')
			self.wumpusDead = True 
			self.removePW() #removes all PW in game board and replaces them with NW
			if not self.retrace: 
				self.moveHistory.pop()
		
		if len(self.moveHistory) > 0: 
			if self.moveHistory[-1] == 'SHOOT' and not self.wumpusDead: #we shot arrow and heard no scream   ##TEST EVERY SCENARIO BY CREATING THE WORLDS 	
		#		print('Just shot and wumpus not dead')
				nbrList = self.gameNodes[(self.x,self.y)]  
				nbrIsWumpus = (len(self.gameNodes[(self.x,self.y)]) == 2) #if only 2 neighbors we know other nbr is for sure a wumpus bc we heard no scream 
				if self.direction == 'Right':
					if 'NW' not in self.gameStates[(self.x+1, self.y)]: self.gameStates[(self.x+1, self.y)].append('NW') 
					if nbrIsWumpus: 
						for nbr in nbrList: 	
							if nbr != (self.x+1, self.y): 
								self.gameStates[(nbr[0],nbr[1])].append('W') 
					
				elif self.direction == 'Left': 
					if 'NW' not in self.gameStates[(self.x-1, self.y)]: self.gameStates[(self.x-1, self.y)].append('NW') 
					if nbrIsWumpus: 
						for nbr in nbrList: 
							if nbr != (self.x-1,self.y):
								self.gameStates[(nbr[0],nbr[1])].append('W') 
				elif self.direction == 'Up': 
					if 'NW' not in self.gameStates[(self.x, self.y+1)]: self.gameStates[(self.x, self.y+1)].append('NW')
					if nbrIsWumpus: 	
						for nbr in nbrList: 
							if nbr != (self.x, self.y+1): 	
								self.gameStates[(nbr[0],nbr[1])].append('W') 
				elif self.direction == 'Down': 
					if 'NW' not in self.gameStates[(self.x, self.y-1)]: self.gameStates[(self.x, self.y-1)].append('NW')
					if nbrIsWumpus: 
						for nbr in nbrList:
							if nbr != (self.x, self.y-1): 
								self.gameStates[(nbr[0],nbr[1])].append('W') 
				if not self.retrace:
					self.moveHistory.pop() #remove shoot from moveHistory so it doesnt interfere with backtracking 

		if stench:
			#print('Stench...')
			if breeze and self.x == 1 and self.y == 1: 
				self.score -= 1
				return Agent.Action.CLIMB		
			if not self.wumpusDead: 
				self.updatePossibleThreat('W')
			if not breeze: 
				self.removeThreat('P')
			if self.hasArrow and not self.wumpusDead and not self.inProgress and not self.retrace: #TODO: Still may shoot out of bounds!  
				self.hasArrow = False
				if self.direction == 'Right' and 'PW' in self.gameStates[(self.x+1, self.y)]: 
					self.gameStates[(self.x+1, self.y)].remove('PW') 
				elif self.direction == 'Left' and 'PW' in self.gameStates[(self.x-1, self.y)]: 
					self.gameStates[(self.x-1, self.y)].remove('PW') 
				elif self.direction == 'Up' and 'PW' in self.gameStates[(self.x, self.y+1)]: 
					self.gameStates[(self.x, self.y+1)].remove('PW') 
				elif self.direction == 'Down' and 'PW' in self.gameStates[(self.x, self.y-1)]: 
					self.gameStates[(self.x, self.y-1)].remove('PW')
				self.moveHistory.append('SHOOT') 
				self.score -= 10
				return Agent.Action.SHOOT
		#	print('In stench; no arrow...continuing')

		if breeze: 
			self.updatePossibleThreat('P') 
			if not stench: 
				self.removeThreat('W') 
		
		if not self.inProgress: 
		#	print('In not self.inProgress')
			bestMove = self.findBestMove() 
			if bestMove == 'climb': 
				self.score -= 1
				return Agent.Action.CLIMB
			self.moves = self.generateChosenStack(bestMove, self.direction)
			self.inProgress = True 
			#print('Exiting not self.inProgress block')

		if self.inProgress: 
		#	print('In self.inProgress')
			if (self.hasGold or self.retrace) and self.x == 1 and self.y == 1: 
				self.score -= 1
				return Agent.Action.CLIMB
		#	print('self.moves: ', self.moves) 
			if len(self.moves) == 1: self.inProgress = False 
			move = self.moves.pop(0)
			self.moveHistory.append(move) 
			agentMove = 'Agent.Action' + '.' + move  
		#	print('STATES: ') 
		#	for nbr in self.gameNodes[(self.x,self.y)]:
			
		#		print(nbr[0],',',nbr[1],': ',self.gameStates[(nbr[0], nbr[1])])
			if move == 'FORWARD': 
				self.updateCoordinates() 
		#	print('Current Dir: ', self.direction)
			self.changeDirection(move) 
		#	print('Next Dir: ', self.direction) 
		#	print('Next Coordinates: ', self.x, ',', self.y)
			self.score -= 1 
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
