import pygame, win32api, win32con, requests, urlparse, random, Config, Utility, Mouse, Row, Button, CheckBox, Form
from bs4 import BeautifulSoup
from pygame import *

class Load:

	def __init__(self):

		self.mouse = Mouse.Load()
		self.audioDict = self.loadAudioDict()
	
		self.rowData = None
		self.initRowElements()
	
		self.tick = 0
		self.tickMax = self.getTickMax()
		self.targetSetClickerButtonIndex = -1
		self.displayCheck = True
		
	def update(self, WINDOW):
	
		if self.rowData.chkActive.selected == True:
			self.tick += 1
			if self.tick >= self.tickMax:
				self.tick = 0
				self.tickMax = self.getTickMax()
				if self.displayCheck == False : self.displayCheck = True
				
				try : self.scrapeRowData()
				except : self.scrapeFailed()
	
		objectList = self.rowData.getObjectList()
		self.processInput(objectList)
		
		if self.displayCheck == True:
			self.rowData.drawScreen(WINDOW, self.mouse, objectList)
			self.displayCheck = False
			
	def getTickMax(self):
	
		if self.rowData.chkFast.selected == True:
			tickMax = random.uniform(0.5, 1.0) * Config.TICK_FAST
		else:
			tickMax = Config.TICK_NORMAL + (random.uniform(0.5, 1.0) * 200)
			
		return tickMax
		
	def scrapeRowData(self):
		
		url = urlparse.urljoin(u'https://twitter.com/', self.rowData.id)  
		result = requests.get(url)
		soup = BeautifulSoup(result.text, 'html.parser')
		contentCount = str(soup.find("span", class_="ProfileNav-value"))
		#contentCount = str(soup.find("span", class_="css-901oao css-bfa6kz r-111h2gw r-1qd0xha r-n6v787 r-16dba41 r-1sf4r6n r-bcqeeo r-qvutc0"))
		contentText = str(soup.find("p", class_="TweetTextSize")).lower()
		
		# Update Count Check #
		newCount = -1
		if 'data-count="' in contentCount:
			indexStart = contentCount.index('data-count="') + 12
			if '"' in contentCount[indexStart::]:
				indexEnd = indexStart + contentCount[indexStart::].index('"')
				strCount = contentCount[indexStart:indexEnd]
				
				if Utility.stringIsNumber(strCount):
					newCount = int(strCount)
					if newCount > 0 and newCount != self.rowData.count:
						oldCount = self.rowData.count
						self.rowData.count = newCount
						
						# Only Trigger Tweet Update On Less Than 7 Tweets Per Update #
						diff = newCount - oldCount
						if diff != 0 and diff <= 7:
							if self.rowData.chkClicker0.selected == True or self.rowData.chkClicker1.selected == True:
								self.triggerClicker(diff, contentText)
							if self.rowData.chkSound.selected == True:
								self.playAudio(diff, contentText)
								
							print("\n" + contentText)
							
		Config.COUNT_COLOR = [0, 0, 180]
				
	def scrapeFailed(self):
	
		self.rowData.chkClicker0.selected = False
		self.rowData.chkClicker1.selected = False
		
		Config.COUNT_COLOR = [80, 20, 20]
				
	def triggerClicker(self, DIFF, TEXT):
	
		if DIFF < 0:
			self.rowData.chkClicker0.selected = False
			self.rowData.chkClicker1.selected = False
			
		elif DIFF > 0:
		
			clickCheck = True
			if self.rowData.chkList[0].selected == True and "<img alt=" not in TEXT and "pic.twitter.com" not in TEXT : clickCheck = False
			elif self.rowData.chkList[1].selected == True and ("<img alt=" in TEXT or "pic.twitter.com" in TEXT) : clickCheck = False
			
			if clickCheck == True and self.rowData.chkTargetString1.selected == True:
				userInput1 = self.rowData.frmTargetString1.userInput.lower()
				if self.rowData.frmTargetString1.searchMode == "Include" and userInput1 != "" and userInput1 not in TEXT : clickCheck = False
				elif self.rowData.frmTargetString1.searchMode == "Exclude" and userInput1 != "" and userInput1 in TEXT : clickCheck = False
			if clickCheck == True and self.rowData.chkTargetString2.selected == True:
				userInput2 = self.rowData.frmTargetString2.userInput.lower()
				if self.rowData.frmTargetString2.searchMode == "Include" and userInput2 != "" and userInput2 not in TEXT : clickCheck = False
				elif self.rowData.frmTargetString2.searchMode == "Exclude" and userInput2 != "" and userInput2 in TEXT : clickCheck = False
			
			if clickCheck == True:
				if self.rowData.chkClicker0.selected == True:
					self.simulatedClick(self.rowData.clickerList[0])
				if self.rowData.chkClicker1.selected == True:
					self.simulatedClick(self.rowData.clickerList[1])
				
	def simulatedClick(self, LOCATION):
	
		win32api.SetCursorPos(LOCATION)
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, LOCATION[0], LOCATION[1], 0, 0)
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, LOCATION[0], LOCATION[1], 0, 0)
			
	def playAudio(self, DIFF, TEXT):
	
		strAlertType = ""
		strAlertName = self.rowData.id
		if DIFF < 0 : strAlertType = "delete"
		elif DIFF > 0 : strAlertType = "alert"
		
		if strAlertType != "":
			if strAlertName == "realdonaldtrump":
				if "fake news" in TEXT : strAlertName = "fake"
				elif "witch hunt!" in TEXT : strAlertName = "witch"
				
			strTargetAudio = strAlertType + "_" + strAlertName
			if strTargetAudio in self.audioDict:
				pygame.mixer.Sound.play(self.audioDict[strTargetAudio])
			else:
				if DIFF < 0 : pygame.mixer.Sound.play(self.audioDict["delete_default"])
				elif DIFF > 0 : pygame.mixer.Sound.play(self.audioDict["alert_default"])
			
	def processInput(self, OBJECT_LIST):
	
		self.mouse.update()
		for event in pygame.event.get():
		
			if event.type == QUIT:
				raise SystemExit
		
			elif event.type == MOUSEMOTION:
				self.displayCheck = True
		
			elif event.type == MOUSEBUTTONDOWN:
				self.mouseClick(OBJECT_LIST)
				self.displayCheck = True
			
			elif event.type == KEYDOWN:
				self.keyboardInput(pygame.key.name(event.key))
				self.displayCheck = True
				
	def mouseClick(self, OBJECT_LIST):
	
		self.targetSetClickerButtonIndex = -1
	
		for object in OBJECT_LIST:
			if self.mouse.hoverCheck([object.rect.left, object.rect.top], [object.rect.width, object.rect.height]):
				
				print(self.rowData.id+"-"+object.id)
				if object.id in ["frmTargetString1", "frmTargetString2"]:
					print("targetString:"+object.userInput+"\n")
				
				if object.type == "Check Box":
					object.click()
					if object.id == "chkActive" and object.selected == True:
						self.scrapeRowData()
						self.tick = 0
						if self.displayCheck == False : self.displayCheck = True
					elif object.id == "chkFast":
						self.tick = 0
						self.tickMax = self.getTickMax()
						
					# Account Check Boxes #
					if object.id == "chkClickerImage" and self.rowData.chkList[0].selected == True:
						if self.rowData.chkList[1].selected == True : self.rowData.chkList[1].selected = False
					elif object.id == "chkClickerNotImage" and self.rowData.chkList[1].selected == True:
						if self.rowData.chkList[0].selected == True : self.rowData.chkList[0].selected = False
				
				elif object.type == "Button" and object.id[0:13] == "btnSetClicker":
					strTargetButtonIndex = object.id[13::]
					if Utility.stringIsNumber(strTargetButtonIndex):
						self.targetSetClickerButtonIndex = int(strTargetButtonIndex)
						
				elif object.type == "Form" and object.id in ["frmTargetString1", "frmTargetString2"]:
					if object.searchMode == "Include":
						object.searchMode = "Exclude"
					elif object.searchMode == "Exclude":
						object.searchMode = "Include"
						
				break
			
	def keyboardInput(self, KEY):
		
		# Spacebar#
		if KEY == "space" and self.targetSetClickerButtonIndex != -1:
			x, y = win32api.GetCursorPos()
			self.rowData.clickerList[self.targetSetClickerButtonIndex] = [x, y]
		
		else:
			for f in [self.rowData.frmTargetCount, self.rowData.frmTargetString1, self.rowData.frmTargetString2]:
				if self.mouse.hoverCheck([f.rect.left, f.rect.top], [f.rect.width, f.rect.height]):
					
					if KEY == "backspace":
						f.backspace()
					elif f.id == "frmTargetCount" and KEY in "0123456789":
						f.getInput(KEY)
					elif f.id in ["frmTargetString1", "frmTargetString2"]:
						f.getInput(KEY)
	
	def loadAudioDict(self):
	
		audioDict = {}
		if Config.TARGET_ACCOUNT == "realdonaldtrump":
			audioDict["alert_realdonaldtrump"] = pygame.mixer.Sound("audio/alert_realdonaldtrump.wav")
			audioDict["delete_realdonaldtrump"] = pygame.mixer.Sound("audio/delete_realdonaldtrump.wav")
			audioDict["alert_fake"] = pygame.mixer.Sound("audio/alert_fake.wav")
			audioDict["alert_witch"] = pygame.mixer.Sound("audio/alert_witch.wav")
		elif Config.TARGET_ACCOUNT == "whitehouse":
			audioDict["alert_whitehouse"] = pygame.mixer.Sound("audio/alert_whitehouse.wav")
			audioDict["delete_whitehouse"] = pygame.mixer.Sound("audio/delete_whitehouse.wav")
		elif Config.TARGET_ACCOUNT == "potus":
			audioDict["alert_potus"] = pygame.mixer.Sound("audio/alert_potus.wav")
			audioDict["delete_potus"] = pygame.mixer.Sound("audio/delete_potus.wav")
		elif Config.TARGET_ACCOUNT == "vp":
			audioDict["alert_vp"] = pygame.mixer.Sound("audio/alert_vp.wav")
			audioDict["delete_vp"] = pygame.mixer.Sound("audio/delete_vp.wav")
		else:
			audioDict["alert_default"] = pygame.mixer.Sound("audio/alert.wav")
			audioDict["delete_default"] = pygame.mixer.Sound("audio/delete.wav")
			
		return audioDict
		
	def initRowElements(self):
		
		self.rowData = Row.Load(Config.TARGET_ACCOUNT)
	
		# Check Boxes #
		targetYMod = 4
		self.rowData.chkActive = CheckBox.Load("chkActive", [8, targetYMod + 6])
		self.rowData.chkSound = CheckBox.Load("chkSound", [8, targetYMod + 28])
		self.rowData.chkSound.selected = True
		self.rowData.chkFast = CheckBox.Load("chkFast", [8, targetYMod + 50])
		self.rowData.chkTargetString1 = CheckBox.Load("chkTargetString1", [120, targetYMod + 30])
		self.rowData.chkTargetString2 = CheckBox.Load("chkTargetString2", [120, targetYMod + 50])
		self.rowData.chkClicker0 = CheckBox.Load("chkClicker0", [264, targetYMod + (Config.ROW_HEIGHT / 2) - Config.CHK_SIZE[1] - 4])
		self.rowData.chkClicker1 = CheckBox.Load("chkClicker1", [264, targetYMod + 12 + (Config.ROW_HEIGHT / 2)])
		self.rowData.chkList.append(CheckBox.Load("chkClickerImage", [390, targetYMod + (Config.ROW_HEIGHT / 2) - Config.CHK_SIZE[1] - 4]))
		self.rowData.chkList.append(CheckBox.Load("chkClickerNotImage", [390, targetYMod + 12 + (Config.ROW_HEIGHT / 2)]))
		
		# Forms #
		self.rowData.frmTargetCount = Form.Load("frmTargetCount", [120, targetYMod + 5])
		self.rowData.frmTargetString1 = Form.Load("frmTargetString1", [141, targetYMod + (Config.ROW_HEIGHT / 2) - 6])
		self.rowData.frmTargetString2 = Form.Load("frmTargetString2", [141, targetYMod + (Config.ROW_HEIGHT / 2) + 14])
		
		# Buttons #
		self.rowData.btnSetClicker0 = Button.Load("btnSetClicker0", [290, targetYMod + (Config.ROW_HEIGHT / 8) - 2])
		self.rowData.btnSetClicker1 = Button.Load("btnSetClicker1", [290, targetYMod + (Config.ROW_HEIGHT / 2) + 4])
		
		# Clickers #
		self.rowData.clickerList.append([0, 0])
		self.rowData.clickerList.append([0, 0])
		