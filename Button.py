import pygame, Config
from pygame import *

class Load:

	def __init__(self, ID, LOCATION):
	
		self.id = ID
		self.type = "Button"
		self.rect = pygame.rect.Rect(LOCATION, Config.BTN_SIZE)
			
		self.surfaceDefault = pygame.Surface(Config.BTN_SIZE)
		self.surfaceDefault.fill(Config.BTN_COLOR)
		self.surfaceHover = pygame.Surface(Config.BTN_SIZE)
		self.surfaceHover.fill(Config.BTN_HOVER_COLOR)
	
	def draw(self, WINDOW, MOUSE):
	
		targetSurface = self.surfaceDefault
		if MOUSE.x in range(self.rect.left, self.rect.left + self.rect.width):
			if MOUSE.y in range(self.rect.top, self.rect.top + self.rect.height):
				targetSurface = self.surfaceHover
		
		WINDOW.blit(targetSurface, [self.rect.left, self.rect.top])
		