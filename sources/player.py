#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import math
import random
from object_settings import *

pygame.mixer.init()
pygame.mixer.music.set_volume(0.5)

class Player:
	def __init__(self):
		self.x = 0
		self.y = 0

		self.gun_x = 0
		self.gun_y = 0

		self.angle = 0
		self.velocity_x = self.velocity_y = 0
		self.speed = 4
		self.health = 1000
		self.max_health = 1000
		self.power_ups = []
		self.default_damage = 50
		self.damage = self.default_damage
		self.grenade_quanity = 1
		self.grenades = []

		self.shoot_sounds = [pygame.mixer.Sound("sounds/player/gun_shoot_1.wav"), pygame.mixer.Sound("sounds/player/gun_shoot_2.wav"), pygame.mixer.Sound("sounds/player/gun_shoot_3.wav")]
		self.power_up_sound = pygame.mixer.Sound("sounds/player/power_up_1.wav")

		for sound in self.shoot_sounds:
			sound.set_volume(0.10)
		self.power_up_sound.set_volume(0.05)

		self.tile_name = 'Player'
		self.font = pygame.font.SysFont('Comic Sans MS', 17)
		self.health_bar = pygame.image.load('images/tanks/health_bar.png')

		self.image = [pygame.image.load('images/tanks/frame_animation/frame_1.png'), pygame.image.load('images/tanks/frame_animation/frame_2.png')]
		self.gun_image = pygame.image.load('images/tanks/tank_gun.png')
		self.grenade_image = pygame.image.load('images/tiles/power_ups/grenade.png')
		self.grenade_image = pygame.transform.scale(self.grenade_image, (32,36))

		self.grenade_indicator = pygame.image.load('images/screens/grenade_power_indicator.png')

		for img in self.image:
			self.image[self.image.index(img)] = pygame.transform.scale(img, (64,64))
		self.gun_image = pygame.transform.scale(self.gun_image, (64 * (13/12), 64 / (9/5)))

		self.image_counter = 0
		self.image_to_blit = self.image[0]
		self.gun_image_to_blit = self.gun_image 

		self.rect = self.image_to_blit.get_rect()
		self.rect.w -= 16
		self.rect.h -= 16
		self.rect.x = 1280/2 - self.rect.w/2
		self.rect.y = 720/2 - self.rect.h/2

		self.gun_rect = self.gun_image_to_blit.get_rect()

		self.gun_rect.x = self.rect.x + self.gun_image.get_width()/4-2
		self.gun_rect.y = self.rect.y + self.gun_image.get_height()/2-2

		self.w = self.image_to_blit.get_width()
		self.h = self.image_to_blit.get_height()

		self.up = self.down = self.left = self.right = False
		self.direction = 'right' 
		self.last_direction = 'right'
		self.down_block = None
		self.cover_block = None
		self.bush_cheked = False

		self.on_finish_line = False
		self.can_ride = True

	def update(self, tiles):
		self.velocity_x = 0
		self.velocity_y = 0
		damage_boosted = False
		speed_boosted = False

		if self.health < 0:
			self.health = 0

		for up in self.power_ups:
			if up.power_name == 'damage':
				self.damage = 100
				damage_boosted = True

			if up.power_name == 'speed':
				speed_boosted = True

		if self.down_block == 'Bush' or self.down_block == 'Water':
			self.speed = 2
		if speed_boosted and self.down_block == None:
			self.speed = 6
		if not(speed_boosted) and self.down_block == None:
			self.speed = 4

		if not(self.right) and not(self.left) and not(self.up) and not(self.down):
			if self.direction != 'none':
				self.last_direction = self.direction
			self.direction = 'none'

		if not(damage_boosted):
			self.damage = self.default_damage

		if self.direction == 'left':
			self.velocity_x -= self.speed
			self.angle = 180

		if self.direction == 'right':
			self.velocity_x += self.speed
			self.angle = 0

		if self.direction == 'up':
			self.velocity_y -= self.speed
			self.angle = 90

		if self.direction == 'down':
			self.velocity_y += self.speed
			self.angle = 270

		for img in range(len(self.image)):
			self.image_to_blit = pygame.transform.rotate(self.image[img], (self.angle))

		if self.left or self.right or self.up or self.down:
			self.image_to_blit = pygame.transform.rotate(self.image[int(self.image_counter/2)], (self.angle))
			self.image_counter += 1
			if self.image_counter >= len(self.image) * 2:
				self.image_counter = 0

		self.gun_image_to_blit = pygame.transform.rotate(self.gun_image, (self.angle))

		if self.direction == 'left':
			self.gun_rect.x = self.rect.x - self.gun_image.get_width()/4-2
			self.gun_rect.y = self.rect.y + self.gun_image.get_height()/2-3

		if self.direction == 'right':
			self.gun_rect.x = self.rect.x + self.gun_image.get_width()/4-2
			self.gun_rect.y = self.rect.y + self.gun_image.get_height()/2-2

		if self.direction == 'up':
			self.gun_rect.x = self.rect.x + self.gun_image.get_width()/4-2
			self.gun_rect.y = self.rect.y - self.gun_image.get_height()/2-2

		if self.direction == 'down':
			self.gun_rect.x = self.rect.x + self.gun_image.get_width()/4-3
			self.gun_rect.y = self.rect.y + self.gun_image.get_height()/2-2

		if self.direction == 'none':
			self.velocity_x = 0
			self.velocity_y = 0

		self.rect.x += self.velocity_x
		self.rect.y += self.velocity_y

		self.x += self.velocity_x
		self.y += self.velocity_y

		self.check_collision(tiles)

		for up in self.power_ups:
			if int(up.up_timer) < 1:
				del self.power_ups[self.power_ups.index(up)]

		if self.health > self.max_health:
			self.health = self.max_health

	def update_position(self):
		self.rect.x += -self.velocity_x
		self.rect.y += -self.velocity_y

		self.x += -self.velocity_x
		self.y += -self.velocity_y

	def update_gun_position(self):		
		if self.last_direction == 'left':
			self.gun_rect.x = self.rect.x - self.gun_image.get_width()/4-2
			self.gun_rect.y = self.rect.y + self.gun_image.get_height()/2-3

		if self.last_direction == 'right':
			self.gun_rect.x = self.rect.x + self.gun_image.get_width()/4-2
			self.gun_rect.y = self.rect.y + self.gun_image.get_height()/2-2

		if self.last_direction == 'up':
			self.gun_rect.x = self.rect.x + self.gun_image.get_width()/4-2
			self.gun_rect.y = self.rect.y - self.gun_image.get_height()/2-2

		if self.last_direction == 'down':
			self.gun_rect.x = self.rect.x + self.gun_image.get_width()/4-3
			self.gun_rect.y = self.rect.y + self.gun_image.get_height()/2-2

	def throw_grenade(self, grenade_throw_power):
		if self.grenade_quanity > 0:
			self.grenades.append(Grenade(self.rect.centerx, self.rect.centery, self.angle, grenade_throw_power))
			self.grenade_quanity -= 1

	def draw(self, win):
		win.blit(self.image_to_blit, (self.rect.x-8, self.rect.y-8))
		win.blit(self.gun_image_to_blit, (self.gun_rect.x-8, self.gun_rect.y-8))
		w, h = pygame.display.get_surface().get_size()				

	def check_collision(self, objects):
		block = True
		for tile in objects:
			colliding = self.rect.colliderect(tile)
			if not(tile.tile_name in non_collision_objects) and colliding:
				if self.velocity_x > 0:
					self.rect.right = tile.rect.left
					block = False
				if self.velocity_x < 0:
					self.rect.left = tile.rect.right
					block = False
				if self.velocity_y > 0:
					self.rect.bottom = tile.rect.top
					block = False
				if self.velocity_y < 0:
					self.rect.top = tile.rect.bottom
					block = False

			if colliding:
				if tile.tile_name == 'Finish':
					self.on_finish_line = True

				if tile.tile_name == 'Power-up':
					tile.delete_me = True
					boost_buffer = []
					self.power_up_sound.play()

					if tile.power_name == 'heal':
						self.health += 250

					if tile.power_name == 'grenade':
						if self.grenade_quanity < 3:
							self.grenade_quanity += 1

					if tile.power_name != 'heal' and tile.power_name != 'grenade':
						self.power_ups.append(tile)
						boost_buffer.append(tile)
						for up in self.power_ups:
							if tile.power_name == up.power_name:
								up.up_timer = tile.up_timer
							else:
								boost_buffer.append(up)
						self.power_ups = boost_buffer

				if (tile.tile_name == 'Bush' or tile.tile_name == 'Water'):
					self.down_block = tile.tile_name
					if tile.tile_name == 'Bush':
						self.cover_block = 'Bush'

				if (tile.tile_name != 'Bush' and tile.tile_name != 'Water'):
					self.down_block = None
					self.cover_block = None
					self.bush_cheked = False

				if tile.tile_name == "Barricade":
					tile.tile_name = "Barricade_Falled"
					tile.health = None
					tile.image = pygame.image.load("images/tiles/barricade_falled.png")
					tile.image = pygame.transform.scale(tile.image, (tile.w, tile.h))
					tile.image = pygame.transform.rotate(tile.image, (tile.angle))

				if tile.tile_name == "Mine":
					self.health -= 150
					tile.health = 0

		self.can_ride = block


class Grenade:
	def __init__(self, x, y, throwed_angle, throw_power):
		self.x = x
		self.y = y

		self.image = pygame.image.load('images/tiles/power_ups/grenade.png')
		self.image_to_blit = pygame.transform.scale(self.image, (24, 32))
		self.rect = self.image_to_blit.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y
		self.tick = 0
		self.angle = random.randint(0, 360)
		self.damage = 300
		self._explode = False

		self.throwed_angle = throwed_angle
		self.speedx, self.speedy = 0, 0
		self.speed = throw_power
		self.angle_speed = 7

	def update(self, obj_x, obj_y):
		self.angle += self.angle_speed
		self.image_to_blit = pygame.transform.rotate(self.image, self.angle)
		self.rect = self.image_to_blit.get_rect(center=self.rect.center)

		self.rect.x = obj_x + self.rect.x
		self.rect.y = obj_y + self.rect.y

		if self.speed > 0:
			if self.throwed_angle == 180:
				self.speedx = -self.speed

			if self.throwed_angle == 0:
				self.speedx = self.speed

			if self.throwed_angle == 90:
				self.speedy = -self.speed

			if self.throwed_angle == 270:
				self.speedy = self.speed

			self.rect.x += self.speedx
			self.rect.y += self.speedy

		self.speed -= 0.1
		if self.angle_speed > 0:
			self.angle_speed -= 0.1

		if self.speed <= 0:
			self.tick += 1

		if self.tick >= 70:
			self._explode = True

	def explode(self, objects, destruct_obj):
		explode_rect = pygame.Rect(self.rect.x-80+self.rect.w/2, self.rect.y-80+self.rect.h/2,160,160)
		for obj in objects:
			if explode_rect.colliderect(obj):
				if obj.health != None and obj.health > 0 and obj.tile_name in destruct_obj:
					obj.health -= self.damage

	def draw(self, win):
		win.blit(self.image_to_blit, self.rect)
