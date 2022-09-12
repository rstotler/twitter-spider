import pygame, Config
from pygame import *

class Load:

	def __init__(self, ID, LOCATION):
	
		self.id = ID
		self.type = "Check Box"
		self.rect = pygame.rect.Rect(LOCATION, Config.CHK_SIZE)
		
		self.surfaceDefault = pygame.Surface(Config.CHK_SIZE)
		self.surfaceDefault.fill(Config.BTN_COLOR)
		self.surfaceHover = pygame.Surface(Config.CHK_SIZE)
		self.surfaceHover.fill(Config.CHK_HOVER_COLOR)
		
		self.selected = False
		
	def draw(self, WINDOW, MOUSE):
	
		targetSurface = self.surfaceDefault
		if MOUSE.x in range(self.rect.left, self.rect.left + self.rect.width):
			if MOUSE.y in range(self.rect.top, self.rect.top + self.rect.height):
				targetSurface = self.surfaceHover
		
		WINDOW.blit(targetSurface, [self.rect.left, self.rect.top])
		if self.selected == True:
			pygame.draw.circle(WINDOW, Config.BACKGROUND_COLOR, [self.rect.left + (self.rect.width / 2), self.rect.top + (self.rect.height / 2)], int(self.rect.width * .30))
				
	def click(self):
	
		if self.selected == False : self.selected = True
		elif self.selected == True : self.selected = False
		