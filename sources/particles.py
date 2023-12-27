#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import random

class Penetration:
	def __init__(self, x, y, angle):
		self.x = x
		self.y = y
		self.tick = 5

		self.images = [pygame.image.load("images/sprites/penetrations/penetration_1.png"), pygame.image.load("images/sprites/penetrations/penetration_2.png")]
		self.rnd_image = random.randint(0, 1)
		self.image = pygame.transform.rotate(self.images[self.rnd_image], angle)

		self.x -= self.image.get_width()/2-1.5
		self.y -= self.image.get_height()/2-1.5

	def update(self, obj_x, obj_y):
		self.x = obj_x + self.x
		self.y = obj_y + self.y
		if self.tick >= 0:
			self.tick -= 1

	def draw(self, win):
		win.blit(self.image, (self.x, self.y))

class Explosion:
	def __init__(self, x, y, w, h):
		self.images = [pygame.image.load("images/sprites/explosion/explosion_1.png"), pygame.image.load("images/sprites/explosion/explosion_2.png"), pygame.image.load("images/sprites/explosion/explosion_3.png")]
		self.current_image = 0
		self.image = pygame.transform.scale(self.images[self.current_image], (w,h))

		self.x = x - self.image.get_width()/2
		self.y = y - self.image.get_height()/2
		self.w = w
		self.h = h
		
		self.tick = 5 * len(self.images)

	def update(self, obj_x, obj_y):
		self.x = obj_x + self.x
		self.y = obj_y + self.y

		self.tick -= 1
		if self.tick % 5 == 0 and self.tick > 0:
			self.current_image += 1
			self.image = pygame.transform.scale(self.images[self.current_image], (self.w, self.h))

	def draw(self, win):
		win.blit(self.image, (self.x, self.y))


