import pygame
from pygame import *

def write(LABEL, LOCATION, COLOR, FONT, WINDOW):

	text = FONT.render(LABEL, True, COLOR)
	WINDOW.blit(text, LOCATION)
	
def outline(WINDOW, COLOR, LOCATION, SIZE):
	
	pygame.draw.line(WINDOW, COLOR, [LOCATION[0], LOCATION[1]], [LOCATION[0] + SIZE[0], LOCATION[1]])
	pygame.draw.line(WINDOW, COLOR, [LOCATION[0], LOCATION[1]], [LOCATION[0], LOCATION[1] + SIZE[1] - 1])
	pygame.draw.line(WINDOW, COLOR, [LOCATION[0] + SIZE[0], LOCATION[1]], [LOCATION[0] + SIZE[0], LOCATION[1] + SIZE[1] - 1])
	pygame.draw.line(WINDOW, COLOR, [LOCATION[0], LOCATION[1] + SIZE[1] - 1], [LOCATION[0] + SIZE[0], LOCATION[1] + SIZE[1] - 1])
	
def stringIsNumber(STRING):

	try:
		int(STRING)
		return True
	except ValueError:
		return False
