#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

class Tile:
	def __init__(self, x, y, w, h, image_directory, tile_name, angle=0):
		self.x = x
		self.y = y
		self.w = w
		self.h = h

		self.tile_name = tile_name
		self.image_directory = image_directory
		self.health = None
		self.angle = angle

		self.image = pygame.image.load(image_directory)
		self.image = pygame.transform.scale(self.image, (self.w, self.h))
		self.image = pygame.transform.rotate(self.image, (angle))
		self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

		self.visibility = True

	def update(self, obj_x, obj_y):
		self.x = obj_x + self.x
		self.y = obj_y + self.y

		self.rect.x = self.x
		self.rect.y = self.y
		self.rect.w = self.w
		self.rect.h = self.h

	def draw(self, win):
		if self.visibility:
			win.blit(self.image, (self.rect.x, self.rect.y, self.rect.w, self.rect.h))

	def check_visibility(self, w, h):
		if self.rect.x + self.rect.w >= 0 and self.rect.x <= w and self.rect.y + self.rect.h >= 0 and self.rect.y <= h:
			self.visibility = True
		else:
			self.visibility = False

	def __del__(self):
		pass
