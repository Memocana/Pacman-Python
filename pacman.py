#PacMan
#copyright: Mehmet Can Alaca
#Hisar Schools
import time
import pygame
from pygame.locals import *
from sys import exit
import math

pygame.init()
screen=pygame.display.set_mode((1024,718),0,32)
pygame.display.set_caption("PacMan!")
pygame.font.init()

back = pygame.Surface((1024,718))
background = back.convert()
background.fill((0,0,0))
old_time=0

myimage = pygame.image.load('pacman.png')
scared = pygame.image.load('scared.png')
eyes = pygame.image.load('eyes.png')
gameOverImage = pygame.image.load('gameover.png')
youwin = pygame.image.load('youwin.png')

blinkyImages = [None, pygame.image.load('blinky1.png'), pygame.image.load('blinky2.png'), pygame.image.load('blinky-2.png'), pygame.image.load('blinky-1.png')]
pinkyImages = [None, pygame.image.load('pinky1.png'), pygame.image.load('pinky2.png'), pygame.image.load('pinky-2.png'), pygame.image.load('pinky-1.png')]
inkyImages = [None, pygame.image.load('inky1.png'), pygame.image.load('inky2.png'), pygame.image.load('inky-2.png'), pygame.image.load('inky-1.png')]
clydeImages = [None, pygame.image.load('clyde1.png'), pygame.image.load('clyde2.png'), pygame.image.load('clyde-2.png'), pygame.image.load('clyde-1.png')]

score = 0
ghost = 0
lives = 3
gameOver = False

grid = [[4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
        [4,3,2,2,2,2,2,2,2,4,4,2,2,2,2,2,2,2,3,4],
        [4,2,4,4,2,4,4,4,2,4,4,2,4,4,4,2,4,4,2,4],
        [4,2,4,4,2,2,2,2,2,2,1,2,2,2,2,2,4,4,2,4],
        [4,2,2,2,2,4,2,4,4,4,4,4,4,2,4,2,2,2,2,4],
        [4,4,4,4,2,4,2,2,2,4,4,2,2,2,4,2,4,4,4,4],
        [0,0,0,4,2,4,4,4,2,4,4,2,4,4,4,2,4,0,0,0],
        [0,0,0,4,2,4,2,2,2,2,2,2,2,2,4,2,4,0,0,0],
        [4,4,4,4,2,4,2,4,4,9,9,4,4,2,4,2,4,4,4,4],
        [2,5,2,2,2,2,2,4,0,0,0,0,4,2,2,2,2,2,6,2],
        [4,4,4,4,2,4,2,4,4,4,4,4,4,2,4,2,4,4,4,4],
        [0,0,0,4,2,4,2,2,2,2,2,2,2,2,4,2,4,0,0,0],
        [0,0,0,4,2,4,2,4,4,4,4,4,4,2,4,2,4,0,0,0],
        [4,4,4,4,2,2,2,2,2,4,4,2,2,2,2,2,4,4,4,4],
        [4,2,2,2,2,4,4,4,2,4,4,2,4,4,4,2,2,2,2,4],
        [4,2,4,4,7,2,2,2,2,2,2,2,2,2,2,8,4,4,2,4],
        [4,2,4,4,2,4,2,4,4,4,4,4,4,2,4,2,4,4,2,4],
        [4,2,4,4,2,4,2,2,2,4,4,2,2,2,4,2,4,4,2,4],
        [4,3,2,2,2,4,4,4,2,2,2,2,4,4,4,2,2,2,3,4],
        [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4]]

pins = [K_RIGHT, K_LEFT, K_UP, K_DOWN, K_d, K_a, K_w, K_s]

class Pac:
	def __init__(self,x,y,direction):
		self.x=x #10
		self.y=y #4
		self.direction=direction
		self.open = True
		self.images = [pygame.image.load('pacman2.png'), myimage, pygame.transform.rotate(myimage,-90), pygame.transform.rotate(myimage, 90), pygame.transform.rotate(myimage,180)]

	def turns(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				exit()
				self.direction = 0
			if event.type == KEYDOWN:
				if event.key == K_RIGHT and self.direction != -1:
					if self.movable(1):
						self.direction = 1
				elif event.key == K_LEFT and self.direction != 1:
					if self.movable(-1):
						self.direction = -1
				elif event.key == K_DOWN and self.direction != -2:
					if self.movable(2):
						self.direction = 2
				elif event.key == K_UP and self.direction != 2:
					if self.movable(-2):
						self.direction = -2    
	def move(self):
		global score
		global ghost
		if self.direction % 2 == 1:
			if grid[self.y][(self.x+self.direction)] < 4:
				self.x += self.direction
				if grid[self.y][self.x] == 2:
					score += 1
				elif grid[self.y][self.x] == 3:
					score += 5 #invinciblity shizz
					ghost = 15
				grid[self.y][(self.x-self.direction)] = 0
				grid[self.y][self.x] = 1
			elif grid[self.y][(self.x+self.direction)] < 9:
				gameOver = True
		elif self.direction % 2 == 0:
			if grid[self.y+self.direction/2][self.x] < 4:
				self.y += self.direction/2
				if grid[self.y][self.x] == 2:
					score += 1
				elif grid[self.y][self.x] == 3:
					score += 5 #invinciblity shizz
					ghost = 15
				grid[self.y-self.direction/2][self.x] = 0
				grid[self.y][self.x%20] = 1
			elif grid[self.y+self.direction/2][self.x] < 9:
				gameOver = True

		if self.x == 19:
			self.x = -1
		elif self.x == -1:
			self.x = 19

	def movable(self, look):
		if look % 2 == 1:
			return grid[self.y][self.x+look] < 4
		return grid[self.y+look / 2][self.x] < 4

	def modifyImage(self):
		global myimage
		if self.open:
			myimage = self.images[self.direction]
		else:
			myimage = self.images[0]
		self.open = not self.open

class Ghosts:
	def __init__(self, x, y, direction, images, name):
		self.x = x
		self.y = y
		self.direction = direction
		self.replacement = 2
		self.name = name
		self.mode = True
		self.fail = 0
		self.dead = False
		self.images = images
		self.image = self.images[direction]

	def checkAlive(self):
		if not self.mode and (grid[self.y][self.x] == 1 or self.replacement == 1) :
			self.dead = True

	def moveFront(self):
		global gameOver

		if self.movable():
			if self.direction % 2 == 1:
				self.x += self.direction
				if (self.replacement < 4 and self.replacement > 1) or self.replacement == 0:
					grid[self.y][(self.x-self.direction)] = self.replacement
				else:
					grid[self.y][(self.x-self.direction) ] = 2
				self.replacement = grid[self.y][self.x]		
			elif self.direction % 2 == 0:
				self.y += self.direction/2
				if (self.replacement < 4 and self.replacement > 1) or self.replacement == 0:
					grid[self.y-self.direction/2][self.x] = self.replacement
				else:
					grid[self.y-self.direction/2][self.x] = 2
				self.replacement = grid[self.y][self.x]

		if grid[self.y+1][self.x] == 9:
			self.dead = False
			
		if self.replacement == 1 and self.mode and not self.dead:
			self.replacement = 2
			gameOver = True

		if self.dead:
			grid[self.y][self.x] = -2
		elif self.mode:
			grid[self.y][self.x] = self.name
		else:
			grid[self.y][self.x] = -1
			
		if self.x == 19:
			self.x = -1
		elif self.x == -1:
			self.x = 19

	def route(self,target):
		#moves = self.directionsAvailable()
		counter = 0
		minDistance = -1
		idealDirection = 0
		for i in self.directionsAvailable():
			dist = 0
			directionToMove = 0
			if i == "1":
				if counter == 0:
					dist = self.calculateRoute(self.x + 1, self.y, target)
					directionToMove = 1
				elif counter == 1:
					dist = self.calculateRoute(self.x, self.y+1, target)
					directionToMove = 2
				elif counter == 2:
					dist = self.calculateRoute(self.x - 1, self.y, target)
					directionToMove = -1
				elif counter == 3:
					dist = self.calculateRoute(self.x, self.y-1, target)
					directionToMove = -2
			if directionToMove != 0 and (dist < minDistance or minDistance == -1) and (target != "run"):
				minDistance = dist
				idealDirection = directionToMove
			elif directionToMove != 0 and dist > minDistance and target == "run":
				minDistance = dist
				idealDirection = directionToMove
			counter += 1
		if (idealDirection != 0):
			self.fail = 0
			return idealDirection
		self.fail += 1
		if (self.fail == 3):
			self.fail = 0
			return -self.direction
		return self.direction

	def directionsAvailable(self):
		directions = ""
		if self.direction % 2 == 1:
			if self.movable() and self.direction == 1:
				directions += "1" #Right
			else:
				directions += "0"
			if grid[self.y+1][self.x % 20] < 4: #Down
				directions += "1"
			else:
				directions += "0"
			if self.movable() and self.direction == -1:
				directions += "1" #Left
			else:
				directions += "0"
			if grid[self.y-1][self.x % 20] < 4: #Up
				directions += "1"
			else:
				directions += "0"
		else:
			if grid[self.y][(self.x+1) % 20] < 4: #Right
				directions += "1"
			else:
				directions += "0"
			if self.movable() and self.direction == 2:
				directions += "1" #Down
			else:
				directions += "0"
			if grid[self.y][(self.x-1) % 20] < 4: #Left
				directions += "1"
			else:
				directions += "0"
			if self.movable() and self.direction == -2:
				directions += "1" #Up
			else:
				directions += "0"
		return directions

	def calculateRoute(self, x, y, target):
		if (target != "home"):
			return math.hypot((pacman.x - x * 1.0),(pacman.y - y*1.0))
		return math.hypot((8 - x * 1.0),(8 - y*1.0))

	def movable(self):
		if self.direction % 2 == 1:
			return grid[self.y][self.x+self.direction] < 4 and grid[self.y][self.x+self.direction] >= 0
		return grid[self.y+self.direction/ 2][self.x] < 4 and grid[self.y+self.direction/ 2][self.x] >= 0

	def move(self):
		if self.dead:
			self.direction = self.route("home")
		elif self.mode:
			self.direction = self.route("pacman")
		else:
			self.direction = self.route("run")
		self.modifyImage()
		self.moveFront()

	def modifyImage(self):
		self.image = self.images[self.direction]

class Pinky(Ghosts):

	def calculateRoute(self, x, y, target):
		if pacman.direction %2 == 1:
			return math.hypot((pacman.x + pacman.direction * 4 - x * 1.0),(pacman.y  - y*1.0))
		return math.hypot((pacman.x  - x * 1.0),(pacman.y + pacman.direction * -2 - y*1.0))

class Clyde(Ghosts):

	def move(self):
		if not self.mode or self.dead:
			Ghosts.move(self)
		else:
			if self.calculateRoute(self.x, self.y, "pacman") > 5:
				self.direction = self.route("pacman")
			else:
				self.direction = self.route("corner")
			self.modifyImage()
			self.moveFront()
		
	def calculateRoute(self, x, y, target):
		if (target == "home"):
			return Ghosts.calculateRoute(self, x, y, target)
		elif (target == "pacman"):
			return math.hypot((pacman.x - x * 1.0),(pacman.y - y*1.0))
		return math.hypot((x * 1.0),(20 - y*1.0))

class Inky(Ghosts):
	def __init__(self,x,y,direction,image,name):
		Ghosts.__init__(self,x,y,direction,image,name) #Missing stuff here

#________________________________________________________________
#main game methods:
def modifyGrid():
	screen.blit(background,(0,0)) 
	pygame.draw.rect(screen,(255,255,255),Rect(192,39,640,640),3) #draws outer frame
	for x in xrange(20):
		for y in xrange(20):
			if (grid[y][x] == 1):
				screen.blit(myimage, Rect(192+x*32+2,39+y*32+2,28,28))
			elif (grid[y][x] == 2):
				pygame.draw.circle(screen,(243, 180, 147),(192+x*32+16, 39+y*32+16),3)
			elif (grid[y][x] == 3):
				pygame.draw.circle(screen,(102, 40, 40),(192+x*32+16, 39+y*32+16),10)
			elif (grid[y][x] == 4):
				pygame.draw.rect(screen,(31, 68, 245),Rect(192+x*32,39+y*32,32,32),3)
			elif (grid[y][x] == 9):
				pygame.draw.rect(screen,(25, 25, 25),Rect(192+x*32,39+y*32,32,32),3)
			elif (grid[y][x] == 5):
				screen.blit(blinky.image, Rect(190+x*32+2,38+y*32+2,28,28))
			elif (grid[y][x] == 6):
				screen.blit(pinky.image, Rect(190+x*32+2,38+y*32+2,28,28))
			elif (grid[y][x] == 7):
				screen.blit(clyde.image, Rect(190+x*32+2,38+y*32+2,28,28))
			elif (grid[y][x] == 8):
				screen.blit(inky.image, Rect(190+x*32+2,38+y*32+2,28,28))
			elif (grid[y][x] == -1):
				screen.blit(scared, Rect(190+x*32+2,38+y*32+2,28,28))
			elif (grid[y][x] == -2):
				screen.blit(eyes, Rect(190+x*32+2,38+y*32+2,28,28))
	for i in range(lives):
		screen.blit(myimage, Rect(20 + 30*i,20,28,28))

def resetGame():
	global blinky
	global pinky
	global inky
	global clyde

	grid[pacman.y][pacman.x] = 0

	grid[blinky.y][blinky.x] = blinky.replacement
	grid[pinky.y][pinky.x] = pinky.replacement
	grid[clyde.y][clyde.x] = clyde.replacement
	grid[inky.y][inky.x] = inky.replacement

	pacman.x, pacman.y = 10, 3
	pacman.direction = 1

	blinky = Ghosts(1,9,1, blinkyImages, 5)
	pinky = Pinky(18,9,-1, pinkyImages, 6)
	clyde = Clyde(4,15,-2, clydeImages, 7)
	inky = Inky(15,15,-2, inkyImages, 8)

def isGridEmpty():
	for i in grid:
		if i.count(2) > 0:
			return True
	return False
	
#________________________________________________________________________________
#initialization: clock and characters

clock = pygame.time.Clock()
initial_time=time.time()
pacman = Pac(10,3,1)#10,3
blinky = Ghosts(1,9,1, blinkyImages, 5)
pinky = Pinky(18,9,-1, pinkyImages, 6)
clyde = Clyde(4,15,-2, clydeImages, 7)
inky = Inky(15,15,-2, inkyImages, 8)

modifyGrid()

while True:
    if lives > 0 and isGridEmpty():
        multiplier=8.5 #must be odd
        current_time=int((time.time()-initial_time)*multiplier)
        if current_time  > old_time:
        	if current_time % 2 == 0:
        		pacman.turns()
   	       		pacman.modifyImage()
   	       		pacman.move()
   	       		blinky.checkAlive()
   	       		pinky.checkAlive()
   	       		clyde.checkAlive()
   	       		inky.checkAlive()

   	       	if current_time % 3 == 0:
   	       		blinky.mode, pinky.mode, clyde.mode, inky.mode = (ghost == 0), (ghost == 0), (ghost == 0), (ghost == 0)
   	       		if ghost != 0:
   	       			ghost -= 1
   	       		
   	       		blinky.move()
   	       		pinky.move()
   	       		clyde.move()
   	       		inky.move()
        	
        	modifyGrid()
        	old_time=current_time
        	if gameOver:
        		resetGame()
        		lives -= 1
        		gameOver = False
    else:
    	multiplier=3 #must be odd
        current_time=int((time.time()-initial_time)*multiplier)
        modifyGrid()

        if current_time % 2 == 0:
        	if lives == 0:
        		screen.blit(gameOverImage, (192,220))
        	elif not isGridEmpty():
        		screen.blit(youwin, (192,220))

    pygame.display.update()

    

            
    
