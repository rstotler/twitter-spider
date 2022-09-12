import pygame
from pygame import *

class Load:

	def __init__(self):
	
		self.x = 0
		self.y = 0
		self.oldX = 0
		self.oldY = 0
		
	def update(self):
	
		self.oldX = self.x
		self.oldY = self.y
		self.x, self.y = pygame.mouse.get_pos()
		
	def hoverCheck(self, TARGET_LOC, TARGET_SIZE):
	
		if self.x in range(TARGET_LOC[0], TARGET_LOC[0] + TARGET_SIZE[0]):
			if self.y in range(TARGET_LOC[1], TARGET_LOC[1] + TARGET_SIZE[1]):
				return True

		return False
		