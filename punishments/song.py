from playsound import playsound
# playsound('./ninja.mp3') # full song

from time import sleep
import pygame
pygame.mixer.init()
pygame.mixer.music.load('./ninja.mp3')
pygame.mixer.music.play() # for 5 seconds
sleep(5)
pygame.mixer.music.stop()