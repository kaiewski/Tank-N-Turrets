#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import random
import math

from particles import *
from object_settings import *

class Bullet:
	def __init__(self, x, y, w, h, damage, angle = 0, turret_gun = False, speed = 20):
		self.x = x
		self.y = y
		self.w = w
		self.h = h

		self.spawn_x, self.spawn_y = 0, 0

		self.speed = speed
		self.speedx = 0
		self.speedy = 0

		self.total_distance = 0 
		self.max_distance = 2000
		self.damage = damage
		self.angle = angle
		self.turret_gun = turret_gun
		self.flight = False
		self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
		self.penetration = None
		self.pen_angle = 0

	def update(self, obj_x, obj_y):
		if self.flight:
			self.rect.x = obj_x + self.rect.x
			self.rect.y = obj_y + self.rect.y	
			self.rect.x += self.speedx
			self.rect.y += self.speedy
			self.total_distance += abs(self.speedx) + abs(self.speedy)
			
			if self.total_distance > self.max_distance:
				self.total_distance = 0
				self.flight = False

		if not(self.flight):
			self.penetration = Penetration(self.rect.x, self.rect.y, self.pen_angle)		
			self.__del__()

	def check_collision(self, objects):
		for obj in objects:
			if self.flight and self.rect.colliderect(obj) and not(obj.tile_name in non_collision_objects):
				if obj.health != None and obj.health > 0:
					obj.health -= self.damage
				self.flight = False

	def shoot(self, obj, sec_obj=None):
		self.speedy = self.speedx = 0
		self.flight = True

		if not(self.turret_gun):
			if obj.angle == 180:
				self.rect.x = obj.gun_rect.x-8
				self.rect.y = obj.gun_rect.y + obj.gun_rect.h/2-1-8
				self.speedx = -self.speed

			if obj.angle == 0:
				self.rect.x = obj.gun_rect.x + obj.gun_rect.w-3-8
				self.rect.y = obj.gun_rect.y + obj.gun_rect.h/2-1-8
				self.speedx = self.speed

			if obj.angle == 90:
				self.rect.x = obj.gun_rect.x + obj.gun_rect.w/4-1-8
				self.rect.y = obj.gun_rect.y-8
				self.speedy = -self.speed

			if obj.angle == 270:
				self.rect.x = obj.gun_rect.x + obj.gun_rect.w/4-1-8
				self.rect.y = obj.gun_rect.y + obj.gun_rect.h*2-3-8
				self.speedy = self.speed

			self.pen_angle = obj.angle
		
		else:
			self.rect.x = obj.rect.centerx + ((obj.rect.w/2+15) * math.sin(math.radians(self.angle)))
			self.rect.y = obj.rect.centery + ((obj.rect.h/2+15) * math.cos(math.radians(self.angle)))

			self.speedx = self.speed * math.sin(math.radians(self.angle))
			self.speedy = self.speed * math.cos(math.radians(self.angle))

			self.pen_angle = self.angle-90

	def draw(self, win):
		pygame.draw.rect(win, (255,255,255), (self.rect.x, self.rect.y, 3, 3))

	def __del__(self):
		pass