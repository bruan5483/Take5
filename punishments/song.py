from playsound import playsound
# playsound('./ninja.mp3') # full song

from time import sleep
import pygame

TIME_LIMIT = 5

pygame.mixer.init()
pygame.mixer.music.load('./ninja.mp3')
pygame.mixer.music.play() 
sleep(TIME_LIMIT)
pygame.mixer.music.stop()