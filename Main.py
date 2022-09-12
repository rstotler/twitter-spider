import pygame, Config, AppData
from pygame import *

'''
    This program was created after Twitter deprecated the TwitterStream API, effectively
    disabling tweet push-notification services for third-party applications. It uses the
    Selenium Webdriver API to scrape a target Twitter user's profile and provide real-time
    updates when a Tweet occurs.
    
    It can also simulate mouse clicks on the screen after determining if certain parameters
    have been met such as whether or not the new tweet contains an image or whether or not
    it contains a particular word or phrase. It also provides the user with ability to determine
    the current number of tweets from any desired starting point.
    
    It was created to help automate trading functions on Predictit.org's tweet futures
    markets (now discontinued).
'''

pygame.init()
window = pygame.display.set_mode(Config.WINDOW_SIZE, 0, 32)
pygame.display.set_caption(Config.CAPTION)
SURFACE_ICON = pygame.image.load("Icon.png").convert_alpha()
pygame.display.set_icon(SURFACE_ICON)
clock = pygame.time.Clock()
appData = AppData.Load()

while True:

	clock.tick(60) / 1000.0
	appData.update(window)
	