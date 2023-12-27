#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

class Button:
	def __init__(self, x, y, w, h, name, file_name, master_volume):
		self.w = w
		self.h = h
		self.name = name

		if 'level_' in self.name:
			self.level = int(name.split('_')[1])
			self.font = pygame.font.SysFont('Comic Sans MS', 100)

		self.image = pygame.image.load(f"images/screens/{file_name}")
		self.image_to_blit = pygame.transform.scale(self.image, (self.w, self.h))
		self.rect = pygame.Rect(x, y, self.image_to_blit.get_width(), self.image_to_blit.get_height())
		self.aimed_sound = pygame.mixer.Sound("sounds/menu/button_aimed.wav")

		self.normal_w = self.rect.w
		self.normal_h = self.rect.h
		self.master_volume = master_volume

		self.aimed = False
		self.checked = False
		self.resized = False

	def update_size(self, offset_x, offset_y):
		if not(self.resized):
			self.rect.x *= offset_x
			self.rect.y *= offset_y
			self.image_to_blit = pygame.transform.scale(self.image, (self.image_to_blit.get_width()*offset_x, self.image_to_blit.get_height()*offset_y))
			self.rect.w = self.normal_w = self.image_to_blit.get_width()
			self.rect.h = self.normal_h = self.image_to_blit.get_height()
			self.resized = True

	def resize(self):
		self.image_to_blit = pygame.transform.scale(self.image, (self.normal_w, self.normal_h))
		self.rect.w = self.normal_w = self.image_to_blit.get_width()
		self.rect.h = self.normal_h = self.image_to_blit.get_height()	

	def update(self):
		if self.aimed:
			self.image_to_blit = pygame.transform.scale(self.image, (self.normal_w*1.2, self.normal_h*1.2))
			if not(self.checked):
				self.aimed_sound.play().set_volume(self.master_volume)
				self.checked = True
		else:
			self.image_to_blit = pygame.transform.scale(self.image, (self.normal_w, self.normal_h))
			self.checked = False

	def draw(self, win):
		win.blit(self.image_to_blit, self.rect)
		if "level_" in self.name:
			info_surface = self.font.render(f'{self.level}', True, (255,255,255))
			win.blit(info_surface, (self.rect.x+40, self.rect.y, self.rect.w, self.rect.h))

class Checkbox:
	def __init__(self, x, y, w, h, name, file_name, text_file_name, text_w, text_h, state=1):
		self.w = w
		self.h = h

		self.text_w = text_w
		self.text_h = text_h

		self.name = name
		self.aimed = False
		self.clicked = False
		self.resized = False

		self.images = [pygame.image.load(f"images/screens/{file_name}_1.png"), pygame.image.load(f"images/screens/{file_name}_2.png")]
		self.state = state
		self.image_to_blit = pygame.transform.scale(self.images[self.state], (w, h))
		self.rect = pygame.Rect(x+self.text_w+100, y+self.w/1.5+3, w, h)

		self.mark_img = pygame.image.load(f"images/screens/check_mark.png")
		self.mark = pygame.transform.scale(self.mark_img, (w+20, h+20))
		self.mark_x, self.mark_y = self.rect.x, self.rect.y-15

		self.text_img = pygame.image.load(f"images/screens/{text_file_name}.png")
		self.text_to_blit = pygame.transform.scale(self.text_img, (text_w, text_h))
		if self.name == "music_checkbox":
			self.text_x, self.text_y = self.rect.x-self.text_w-100, self.rect.y-self.h/1.5-3
		else:
			self.text_x, self.text_y = self.rect.x-self.text_w-100, self.rect.y+self.h/3-3

	def update(self):
		if self.aimed:
			self.image_to_blit = pygame.transform.scale(self.images[1], (self.w, self.h))
		else:
			self.image_to_blit = pygame.transform.scale(self.images[0], (self.w, self.h))
			self.clicked = False

	def update_size(self, offset_x, offset_y):
		if not(self.resized):
			self.image_to_blit = pygame.transform.scale(self.images[self.state], (self.image_to_blit.get_width()*offset_x, self.image_to_blit.get_height()*offset_y))
			self.text_to_blit = pygame.transform.scale(self.text_img, (self.text_to_blit.get_width()*offset_x, self.text_to_blit.get_height()*offset_y))
			self.rect.w = self.image_to_blit.get_width()
			self.rect.h = self.image_to_blit.get_height()

			self.rect.x *= offset_x
			self.rect.y *= offset_y
			self.mark_x, self.mark_y = self.rect.x, self.rect.y-(15*offset_y)
			if self.name == "music_checkbox":
				self.text_x, self.text_y = self.text_x*offset_x, self.rect.y-self.rect.w/(1.5*offset_y)-(3*offset_y)
			else:
				self.text_x, self.text_y = self.text_x*offset_x, self.text_y*offset_y
			self.resized = True


	def change_self_state(self):
		if self.state == 0:
			self.state = 1
		elif self.state == 1:
			self.state = 0
		self.clicked = True

	def draw(self, win):
		win.blit(self.image_to_blit, self.rect)
		win.blit(self.text_to_blit, (self.text_x, self.text_y, self.text_w, self.text_h))

		if self.state == 1:
			win.blit(self.mark, (self.mark_x, self.mark_y, self.rect.w, self.rect.h))
