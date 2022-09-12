import pygame, Config, Utility
from pygame import *

class Load:

	def __init__(self, ID):
	
		self.id = ID
		self.count = -1
		
		self.font_s = pygame.font.SysFont("Font/"+Config.FONT_PATH+".ttf", Config.FONT_SIZE_S)
		self.font_m = pygame.font.SysFont("Font/"+Config.FONT_PATH+".ttf", Config.FONT_SIZE_M)
		self.font_l = pygame.font.SysFont("Font/"+Config.FONT_PATH+".ttf", Config.FONT_SIZE_L)
		
		# Interactive Elements #
		self.chkActive = None
		self.chkSound = None
		self.chkFast = None
		self.chkTargetString1 = None
		self.chkTargetString2 = None
		self.chkClicker0 = None
		self.chkClicker1 = None
		self.frmTargetCount = None
		self.frmTargetString1 = None
		self.frmTargetString2 = None
		self.btnSetClicker0 = None
		self.btnSetClicker1 = None
		
		self.chkList = []
		self.clickerList = []
		
	def getObjectList(self):
	
		objectList = []
		
		if self.chkActive != None : objectList.append(self.chkActive)
		if self.chkSound != None : objectList.append(self.chkSound)
		if self.chkFast != None : objectList.append(self.chkFast)
		if self.chkTargetString1 != None : objectList.append(self.chkTargetString1)
		if self.chkTargetString2 != None : objectList.append(self.chkTargetString2)
		if self.chkClicker0 != None : objectList.append(self.chkClicker0)
		if self.chkClicker1 != None : objectList.append(self.chkClicker1)
		if self.frmTargetCount != None : objectList.append(self.frmTargetCount)
		if self.frmTargetString1 != None : objectList.append(self.frmTargetString1)
		if self.frmTargetString2 != None : objectList.append(self.frmTargetString2)
		if self.btnSetClicker0 != None : objectList.append(self.btnSetClicker0)
		if self.btnSetClicker1 != None : objectList.append(self.btnSetClicker1)
		for chk in self.chkList : objectList.append(chk)
		
		return objectList
		
	def drawScreen(self, WINDOW, MOUSE, OBJECT_LIST):
	
		WINDOW.fill(Config.BACKGROUND_COLOR)
		Utility.outline(WINDOW, Config.OUTLINE_COLOR, [4, 4], [Config.WINDOW_SIZE[0] - 8, Config.WINDOW_SIZE[1] - 8])
		
		for object in OBJECT_LIST:
			object.draw(WINDOW, MOUSE)
		
		targetYMod = 4
		
		Utility.write("Actv.", [26, 10 + targetYMod], Config.FONT_COLOR, self.font_s, WINDOW)
		Utility.write("Aud.", [26, 32 + targetYMod], Config.FONT_COLOR, self.font_s, WINDOW)
		Utility.write("Fast", [26, 53 + targetYMod], Config.FONT_COLOR, self.font_s, WINDOW)
		
		STR_ID = self.id
		if STR_ID == "realdonaldtrump" : STR_ID = "rdt"
		elif STR_ID == "whitehouse" : STR_ID = "wh"
		elif STR_ID == "_spacephish" : STR_ID = "_sp"
		Utility.write(STR_ID, [195, targetYMod + 5], Config.FONT_COLOR, self.font_m, WINDOW)
		
		minusNum = 0
		if len(self.frmTargetCount.userInput) > 0 and Utility.stringIsNumber(self.frmTargetCount.userInput) : minusNum = int(self.frmTargetCount.userInput)
		STR_COUNT = str(self.count - minusNum)
		pygame.draw.circle(WINDOW, Config.COUNT_COLOR, [84, targetYMod + 36], 31)
		Utility.write(STR_COUNT, [58, targetYMod + 15], Config.FONT_COLOR, self.font_l, WINDOW)
		
		Utility.write("Click 1", [258, 6 + targetYMod], Config.FONT_COLOR, self.font_s, WINDOW)
		Utility.write("Click 2", [258, 38 + targetYMod], Config.FONT_COLOR, self.font_s, WINDOW)
		Utility.write("Set", [self.btnSetClicker0.rect.left + 2, self.btnSetClicker0.rect.top + 4], Config.FONT_COLOR, self.font_m, WINDOW)
		Utility.write("Set", [self.btnSetClicker1.rect.left + 2, self.btnSetClicker1.rect.top + 4], Config.FONT_COLOR, self.font_m, WINDOW)
		Utility.write(str(self.clickerList[0]), [335, 16 + targetYMod], Config.FONT_COLOR, self.font_s, WINDOW)
		Utility.write(str(self.clickerList[1]), [335, 48 + targetYMod], Config.FONT_COLOR, self.font_s, WINDOW)
		
		# Extra Clickers #
		Utility.write("Image", [386, 6 + targetYMod], Config.FONT_COLOR, self.font_s, WINDOW)
		Utility.write("Not Image", [379, 38 + targetYMod], Config.FONT_COLOR, self.font_s, WINDOW)
		
		pygame.display.flip()
		