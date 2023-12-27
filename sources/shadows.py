#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

class Shadow:
	def __init__(self, x, y, w, h, color):
		self.surface = pygame.Surface((w, h), pygame.SRCALPHA)
		self.color = color
		self.surface.fill((self.color))

		self.x = x
		self.y = y

	def update(self, x, y):
		self.x = x
		self.y = y

	def draw(self, win):
		win.blit(self.surface, (self.x, self.y))