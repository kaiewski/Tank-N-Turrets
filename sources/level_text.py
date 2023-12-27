#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

pygame.init()
pygame.font.init()

class Level_text:
	def __init__(self, x, y, size, text):
		self.x = x
		self.y = y

		self.normal_x = x
		self.normal_y = y

		self.font = pygame.font.SysFont('Arial', size)
		self.text = self.font.render(text, True, (255,255,255))

	def update(self, obj_x, obj_y):
		self.x = obj_x + self.x
		self.y = obj_y + self.y

	def update_pos(self):
		self.normal_x = self.x
		self.normal_y = self.y

	def draw(self, win):
		pygame.draw.rect(win, (60, 20, 100), (self.x-22, self.y+2, 20, 20))
		win.blit((self.text), (self.x, self.y))