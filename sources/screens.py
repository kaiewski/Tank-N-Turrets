#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

pygame.mixer.init()
pygame.mixer.music.set_volume(0.5)

class Stealth_screen:
	def __init__(self, w, h):
		self.default_image = pygame.image.load('images/screens/stealth_screen.png')
		self.image = self.default_image

		self.up_rect = self.image.get_rect()
		self.down_rect = self.image.get_rect()

		self.up_rect.y = 0-self.image.get_height()
		self.up_rect.w = w
		self.down_rect.y = h
		self.down_rect.w = w

		self.up_y = self.up_rect.y
		self.down_y = self.down_rect.y

		self.player_movement_sound = pygame.mixer.Sound("sounds/player/bush_movement_effect.wav")
		self.player_movement_sound.set_volume(0.05)
		self.bush_cheked = False

		self.on_screen = False
		self.max_point = 70
		self.cur_point = 0
		self.speed = 2

	def update(self):
		if self.on_screen:
			if self.cur_point < self.max_point:
				self.up_y = self.up_rect.y + self.cur_point 
				self.down_y = self.down_rect.y - self.cur_point
				self.cur_point += self.speed
				if not(self.bush_cheked):
					self.player_movement_sound.play()
					self.bush_cheked = True

		if not(self.on_screen):
			if self.cur_point > 0:
				self.up_y = self.up_rect.y + self.cur_point 
				self.down_y = self.down_rect.y - self.cur_point
				self.cur_point -= self.speed
				self.bush_cheked = False

	def update_size(self, w, h):
		self.image = pygame.transform.scale(self.default_image, (w, self.image.get_height()))

		self.up_rect = self.image.get_rect()
		self.down_rect = self.image.get_rect()

		self.up_rect.y = 0-self.image.get_height()
		self.up_rect.w = w

		self.down_rect.y = h
		self.down_rect.w = w

		self.up_y = self.up_rect.y
		self.down_y = self.down_rect.y

	def draw(self, win):
		if self.cur_point > 0:
			win.blit(pygame.transform.rotate(self.image, 180), (self.up_rect.x, self.up_y, self.up_rect.w, self.up_rect.h))
			win.blit(self.image, (self.down_rect.x, self.down_y, self.down_rect.w, self.down_rect.h))

class Main_menu_theme:
	def __init__(self, w, h, file_name):
		self.w = w
		self.h = h
		self.image = pygame.image.load(f"images/screens/{file_name}")
		self.image_to_blit = pygame.transform.scale(self.image, (self.w, self.h))
		self.rect = self.image_to_blit.get_rect()

		self.alpha = 100
		self.alpha_speed = 3

	def update(self):
		if self.alpha >= 0 and self.alpha <= 100:
			self.alpha -= self.alpha_speed
			self.image_to_blit.set_alpha(255/100*self.alpha)

	def update_size(self, offset_x, offset_y):
		self.image_to_blit = pygame.transform.scale(self.image, (offset_x, offset_y))
		self.alpha = 100

	def draw(self, win):
		win.blit(self.image_to_blit, self.rect)