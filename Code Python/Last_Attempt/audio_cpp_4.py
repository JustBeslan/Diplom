import pygame

pygame.init()
song = pygame.mixer.Sound('/home/beslan/audio.wav')
clock = pygame.time.Clock()
song.play()
while True:
	clock.tick(60)
pygame.quit()