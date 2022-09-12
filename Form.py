import pygame, Config, Utility
from pygame import *

class Load:

	def __init__(self, ID, LOCATION):
	
		self.id = ID
		self.type = "Form"
		FRM_SIZE = Config.FRM_SIZE[0]
		if self.id in ["frmTargetString1","frmTargetString2"] : FRM_SIZE = Config.FRM_SIZE[1]
		self.rect = pygame.rect.Rect(LOCATION, FRM_SIZE)
		if self.id == "frmTargetCount" : self.font = pygame.font.SysFont("Font/"+Config.FONT_PATH+".ttf", Config.FONT_SIZE_M)
		else : self.font = pygame.font.SysFont("Font/"+Config.FONT_PATH+".ttf", Config.FONT_SIZE_MM)
		self.userInput = ""
		self.searchMode = "Include"
		
		self.surfaceDefault = pygame.Surface(FRM_SIZE)
		self.surfaceDefault.fill(Config.FRM_COLOR)
		self.surfaceDefault2 = pygame.Surface(FRM_SIZE)
		self.surfaceDefault2.fill(Config.FRM_COLOR_2)
		self.surfaceHover = pygame.Surface(FRM_SIZE)
		self.surfaceHover.fill(Config.FRM_HOVER_COLOR)
		
	def draw(self, WINDOW, MOUSE):
	
		targetSurface = self.surfaceDefault
		if self.searchMode == "Exclude":
			targetSurface = self.surfaceDefault2
		
		if MOUSE.x in range(self.rect.left, self.rect.left + self.rect.width):
			if MOUSE.y in range(self.rect.top, self.rect.top + self.rect.height):
				targetSurface = self.surfaceHover
		
		WINDOW.blit(targetSurface, [self.rect.left, self.rect.top])
		
		if len(self.userInput) > 0:
			STR_USERINPUT = self.userInput
			if len(STR_USERINPUT) > 9:
				STR_USERINPUT = ".." + STR_USERINPUT[-9::]
			Utility.write(STR_USERINPUT, [2 + self.rect.left, 2 + self.rect.top], Config.FONT_COLOR, self.font, WINDOW)
			
	def getInput(self, KEY):
	
		if self.id == "frmTargetCount":
			if len(self.userInput) < 5:
				self.userInput = self.userInput + KEY
				
		elif self.id in ["frmTargetString1", "frmTargetString2"]:
			
			# Get Target Key Character #
			key = None
			targetAlphabetDict = Config.ALPHABET_DICT
			if pygame.key.get_mods() & KMOD_SHIFT:
				targetAlphabetDict = Config.ALPHABET_SHIFT_DICT
			if KEY in targetAlphabetDict:
				key = targetAlphabetDict[KEY]
				self.userInput = self.userInput + key
			
	def backspace(self):
	
		if len(self.userInput) > 0:
			self.userInput = self.userInput[:-1]
		