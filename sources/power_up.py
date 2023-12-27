#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

class Power_up:
	def __init__(self, x, y, w, h, image_directory, power_name):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.power_name = power_name
		self.tile_name = 'Power-up'
		self.up_timer = 15
		self.tick = 0

		self.delete_me = False
		self.font = pygame.font.SysFont('Comic Sans MS', 17)

		self.image = pygame.image.load(image_directory)
		self.image = pygame.transform.scale(self.image, (self.w, self.h))
		self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

	def update(self, obj_x, obj_y):
		self.x = obj_x + self.x
		self.y = obj_y + self.y

		self.rect.x = self.x
		self.rect.y = self.y
		self.rect.w = self.w
		self.rect.h = self.h

	def update_timer(self, fps):
		if self.power_name != 'rocket':
			self.tick += 1 
			if self.tick // fps:
				self.up_timer -= 1
				self.tick = 0
			if self.up_timer < 1:
				self.__del__()

	def draw(self, win):
		win.blit(self.image, self.rect)

	def __del__(self):
		pass