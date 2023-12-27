#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import math
import random

from bullet import *

pygame.mixer.init()

class Enemy_Turret:
	def __init__(self, x, y, health, path, angle=0):
		self.x = x
		self.y = y 
		self.health = health
		self.max_health = health
		self.max_range_distance = 4
		self.range_distance = self.max_range_distance
		self.visibility = True
		self.tile_name = 'Static Turret'

		self.angle = angle
		self.reload_tick = 0
		self.fixed_on = None
		self.damage = 50
		self.max_reload = 10
		self.bullet_speed = 30

		self.shoot_sounds = [pygame.mixer.Sound("sounds/static_turret/turret_shoot_1.wav"), pygame.mixer.Sound("sounds/static_turret/turret_shoot_2.wav"), pygame.mixer.Sound("sounds/static_turret/turret_shoot_3.wav")]
		for sound in self.shoot_sounds:
			sound.set_volume(0.05)

		self.image = pygame.image.load(f'''{path}/tiles/enemies/static_turret/static_turret_base.png''')
		self.image = pygame.transform.scale(self.image, (64,64))
		self.gun_image = pygame.image.load(f'''{path}/tiles/enemies/static_turret/static_turret_gun.png''')
		self.gun_image = pygame.transform.scale(self.gun_image, (64 * (26/24), 64 / (26/20)))
		self.gun_image_to_blit = pygame.transform.rotate(self.gun_image, self.angle+90)

		self.rect = self.image.get_rect()
		self.gun_rect = self.gun_image.get_rect()
		self.gun_rect = pygame.Rect(self.gun_rect.x, self.gun_rect.y, 64,64)

		self.w = self.image.get_width()
		self.h = self.image.get_height()

		self.cover_to_range = {
								'Bush': 2,
							}

	def draw(self, win):
		if self.visibility:
			win.blit(self.image, self.rect)
			win.blit(self.gun_image_to_blit, self.gun_rect.topleft)
			# pygame.draw.rect(win, (128, 128, 128), (self.rect.centerx-20, self.rect.centery+20, 40, 5))
			# pygame.draw.rect(win, (90,255,60), (self.rect.centerx-20, self.rect.centery+20, (self.health / self.max_health) * 40, 5))

	def update(self, obj_x, obj_y):
		self.x = obj_x + self.x
		self.y = obj_y + self.y

		self.rect.x = self.x
		self.rect.y = self.y
		self.rect.w = self.w
		self.rect.h = self.h

		self.gun_rect.x = self.rect.x - 16
		self.gun_rect.y = self.rect.y + 8

	def shoot(self):
		if self.fixed_on != None and self.health > 0 and self.reload_tick <= 0:
			bullets = [Bullet(0, 0, 3, 3, self.damage,self.angle, True, self.bullet_speed)]
			for i in bullets:
				i.shoot(self, self.fixed_on)
			self.shoot_sounds[random.randrange(0,3)].play()
			self.reload_tick = self.max_reload
			return bullets
		self.reload_tick -= 1
		return None

	def update_rotate(self, obj):
		dx, dy = int(obj.rect.centerx - self.rect.centerx), int(obj.rect.centery - self.rect.centery)
		distance = int(math.sqrt(dx**2 + dy**2)/64)

		if obj.cover_block != None:
			self.range_distance = self.max_range_distance-self.cover_to_range[obj.cover_block]
		else:
			self.range_distance = self.max_range_distance

		if distance < self.range_distance:
			self.fixed_on = obj
			self.angle = math.degrees(math.atan2(obj.rect.centerx - self.rect.centerx, obj.rect.centery - self.rect.centery))
			self.gun_image_to_blit = pygame.transform.rotate(self.gun_image, self.angle+90)
		else:
			self.fixed_on = None

		self.gun_rect = self.gun_image_to_blit.get_rect(center=self.gun_rect.center)
		self.gun_rect = pygame.Rect(self.gun_rect.x+32, self.gun_rect.y+8, 32,32)

	def check_visibility(self, w, h):
		if self.rect.x + self.rect.w >= 0 and self.rect.x <= w and self.rect.y + self.rect.h >= 0 and self.rect.y <= h:
			self.visibility = True
		else:
			self.visibility = False

class Enemy_Machinegun:
	def __init__(self, x, y, health, path, angle=0):
		self.x = x
		self.y = y 
		self.health = health
		self.max_health = health
		self.max_range_distance = 4
		self.range_distance = self.max_range_distance
		self.visibility = True
		self.tile_name = 'Machine gun'

		self.angle = angle
		self.reload_tick = 0
		self.fixed_on = None
		self.damage = 10
		self.max_reload = 5
		self.bullet_speed = 30

		self.shoot_sound = pygame.mixer.Sound("sounds/machine_gun/machine_gun_shoot_1.wav")
		self.shoot_sound.set_volume(0.05)

		self.image = pygame.image.load(f'''{path}/tiles/enemies/machinegun/machinegun_base.png''')
		self.image = pygame.transform.scale(self.image, (64,64))
		self.gun_image = pygame.image.load(f'''{path}/tiles/enemies/machinegun/machinegun_gun.png''')
		self.gun_image = pygame.transform.scale(self.gun_image, (64 * (26/24), 64 / (26/20)))
		self.gun_image_to_blit = pygame.transform.rotate(self.gun_image, self.angle+90)

		self.rect = self.image.get_rect()
		self.gun_rect = self.gun_image.get_rect()
		self.gun_rect = pygame.Rect(self.gun_rect.x, self.gun_rect.y, 64,64)

		self.w = self.image.get_width()
		self.h = self.image.get_height()

		self.cover_to_range = {
								'Bush': 2,
							}

	def draw(self, win):
		if self.visibility:
			win.blit(self.image, self.rect)
			win.blit(self.gun_image_to_blit, self.gun_rect.topleft)
			
	def update(self, obj_x, obj_y):
		self.x = obj_x + self.x
		self.y = obj_y + self.y

		self.rect.x = self.x
		self.rect.y = self.y
		self.rect.w = self.w
		self.rect.h = self.h

		self.gun_rect.x = self.rect.x - 16
		self.gun_rect.y = self.rect.y + 8

	def shoot(self):
		if self.fixed_on != None and self.health > 0 and self.reload_tick <= 0:
			bullets = [Bullet(0, 0, 3, 3, self.damage,self.angle, True, self.bullet_speed)]
			for i in bullets:
				i.shoot(self, self.fixed_on)
			self.reload_tick = self.max_reload
			self.shoot_sound.play()
			return bullets
		self.reload_tick -= 1
		return None

	def update_rotate(self, obj):
		dx, dy = int(obj.rect.centerx - self.rect.centerx), int(obj.rect.centery - self.rect.centery)
		distance = int(math.sqrt(dx**2 + dy**2)/64)

		if obj.cover_block != None:
			self.range_distance = self.max_range_distance-self.cover_to_range[obj.cover_block]
		else:
			self.range_distance = self.max_range_distance

		if distance < self.range_distance:
			self.fixed_on = obj
			self.angle = math.degrees(math.atan2(obj.rect.centerx - self.rect.centerx, obj.rect.centery - self.rect.centery))
			self.gun_image_to_blit = pygame.transform.rotate(self.gun_image, self.angle+90)
		else:
			self.fixed_on = None

		self.gun_rect = self.gun_image_to_blit.get_rect(center=self.gun_rect.center)
		self.gun_rect = pygame.Rect(self.gun_rect.x+32, self.gun_rect.y+8, 32,32)

	def check_visibility(self, w, h):
		if self.rect.x + self.rect.w >= 0 and self.rect.x <= w and self.rect.y + self.rect.h >= 0 and self.rect.y <= h:
			self.visibility = True
		else:
			self.visibility = False

class Enemy_Launcher:
	def __init__(self, x, y, health, path, angle=0):
		self.x = x
		self.y = y 
		self.health = health
		self.max_health = health
		self.max_range_distance = 4
		self.range_distance = self.max_range_distance
		self.visibility = True
		self.tile_name = 'Launcher'

		self.angle = angle
		self.reload_tick = 0
		self.fixed_on = None
		self.damage = 100
		self.max_reload = 100
		self.bullet_speed = 30

		self.shoot_sound = pygame.mixer.Sound("sounds/grenade_launcher/grenade_launcher_shoot_1.wav")
		self.shoot_sound.set_volume(0.05)

		self.image = pygame.image.load(f'''{path}/tiles/enemies/grenade_launcher/grenade_launcher_base.png''')
		self.image = pygame.transform.scale(self.image, (64,64))
		self.gun_image = pygame.image.load(f'''{path}/tiles/enemies/grenade_launcher/grenade_launcher_gun.png''')
		self.gun_image = pygame.transform.scale(self.gun_image, (64 * (26/24), 64 / (26/20)))
		self.gun_image_to_blit = pygame.transform.rotate(self.gun_image, self.angle)

		self.rect = self.image.get_rect()
		self.gun_rect = self.gun_image.get_rect()
		self.gun_rect = pygame.Rect(self.gun_rect.x, self.gun_rect.y, 64,64)

		self.w = self.image.get_width()
		self.h = self.image.get_height()

		self.cover_to_range = {
								'Bush': 2,
							}

	def draw(self, win):
		if self.visibility:
			win.blit(self.image, self.rect)
			win.blit(self.gun_image_to_blit, self.gun_rect.topleft)

	def update(self, obj_x, obj_y):
		self.x = obj_x + self.x
		self.y = obj_y + self.y

		self.rect.x = self.x
		self.rect.y = self.y
		self.rect.w = self.w
		self.rect.h = self.h

		self.gun_rect.x = self.rect.x - 16
		self.gun_rect.y = self.rect.y + 8

	def shoot(self):
		if self.fixed_on != None and self.health > 0 and self.reload_tick <= 0:
			bullets = [Bullet(0, 0, 3, 3, self.damage,self.angle, True, self.bullet_speed)]
			for i in bullets:
				i.shoot(self, self.fixed_on)
			self.reload_tick = self.max_reload
			self.shoot_sound.play()
			return bullets
		self.reload_tick -= 1
		return None

	def update_rotate(self, obj):
		dx, dy = int(obj.rect.centerx - self.rect.centerx), int(obj.rect.centery - self.rect.centery)
		distance = int(math.sqrt(dx**2 + dy**2)/64)

		if obj.cover_block != None:
			self.range_distance = self.max_range_distance-self.cover_to_range[obj.cover_block]
		else:
			self.range_distance = self.max_range_distance

		if distance < self.range_distance:
			self.fixed_on = obj
			self.angle = math.degrees(math.atan2(obj.rect.centerx - self.rect.centerx, obj.rect.centery - self.rect.centery))
			self.gun_image_to_blit = pygame.transform.rotate(self.gun_image, self.angle+90)
		else:
			self.fixed_on = None

		self.gun_rect = self.gun_image_to_blit.get_rect(center=self.gun_rect.center)
		self.gun_rect = pygame.Rect(self.gun_rect.x+32, self.gun_rect.y+8, 32,32)

	def check_visibility(self, w, h):
		if self.rect.x + self.rect.w >= 0 and self.rect.x <= w and self.rect.y + self.rect.h >= 0 and self.rect.y <= h:
			self.visibility = True
		else:
			self.visibility = False
