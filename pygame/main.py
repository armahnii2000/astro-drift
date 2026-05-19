"""Astro Drift — PyGame edition.

Drifting-ship demo with screen wrap, thrust, rotation, and bullets.
Mirrors the Godot/Love 2D versions for engine-to-engine comparison.
"""

import math
import random
import sys

import pygame

W, H = 960, 540
THRUST = 350.0
ROT_SPEED = 4.0
DRAG_PER_SEC = 0.55
MAX_SPEED = 480.0
BULLET_SPEED = 700.0
BULLET_LIFE = 1.0
SHOOT_COOLDOWN = 0.18


def rotate(point, rot):
	cs, sn = math.cos(rot), math.sin(rot)
	return point[0] * cs - point[1] * sn, point[0] * sn + point[1] * cs


def main() -> None:
	pygame.init()
	screen = pygame.display.set_mode((W, H))
	pygame.display.set_caption("Astro Drift — PyGame")
	clock = pygame.time.Clock()
	font = pygame.font.SysFont("consolas", 16)

	stars = [(random.uniform(0, W), random.uniform(0, H), random.uniform(0.3, 1.0)) for _ in range(80)]

	x, y = W / 2, H / 2
	vx, vy = 0.0, 0.0
	rot = 0.0
	cooldown = 0.0
	bullets: list[list[float]] = []  # [x, y, vx, vy, life]

	while True:
		dt = clock.tick(60) / 1000.0
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()

		keys = pygame.key.get_pressed()
		if keys[pygame.K_a] or keys[pygame.K_LEFT]:
			rot -= ROT_SPEED * dt
		if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
			rot += ROT_SPEED * dt
		thrusting = keys[pygame.K_w] or keys[pygame.K_UP]
		if thrusting:
			vx += math.cos(rot - math.pi / 2) * THRUST * dt
			vy += math.sin(rot - math.pi / 2) * THRUST * dt
		damping = DRAG_PER_SEC ** dt
		vx *= damping
		vy *= damping
		sp = math.hypot(vx, vy)
		if sp > MAX_SPEED:
			vx, vy = vx / sp * MAX_SPEED, vy / sp * MAX_SPEED
		x = (x + vx * dt) % W
		y = (y + vy * dt) % H

		cooldown -= dt
		if (keys[pygame.K_SPACE] or keys[pygame.K_j]) and cooldown <= 0.0:
			cooldown = SHOOT_COOLDOWN
			dx, dy = math.cos(rot - math.pi / 2), math.sin(rot - math.pi / 2)
			bullets.append([x + dx * 18, y + dy * 18, dx * BULLET_SPEED, dy * BULLET_SPEED, BULLET_LIFE])

		for b in bullets:
			b[0] = (b[0] + b[2] * dt) % W
			b[1] = (b[1] + b[3] * dt) % H
			b[4] -= dt
		bullets = [b for b in bullets if b[4] > 0]

		screen.fill((10, 13, 23))
		for sx, sy, br in stars:
			c = int(br * 255)
			screen.set_at((int(sx), int(sy)), (c, c, c))
		for b in bullets:
			pygame.draw.circle(screen, (255, 240, 140), (int(b[0]), int(b[1])), 3)

		hull = [(0, -14), (10, 12), (0, 6), (-10, 12)]
		world = [(x + p[0] * math.cos(rot) - p[1] * math.sin(rot),
		          y + p[0] * math.sin(rot) + p[1] * math.cos(rot)) for p in hull]
		pygame.draw.polygon(screen, (230, 242, 255), world)
		pygame.draw.polygon(screen, (140, 192, 255), world, 2)
		if thrusting:
			flame = [(-5, 8), (0, 18 + random.uniform(0, 6)), (5, 8)]
			flame_world = [(x + p[0] * math.cos(rot) - p[1] * math.sin(rot),
			                y + p[0] * math.sin(rot) + p[1] * math.cos(rot)) for p in flame]
			pygame.draw.polygon(screen, (255, 153, 51), flame_world)

		hud = font.render("Astro Drift — PyGame  |  WASD/arrows fly, Space fires, Esc quits", True, (220, 230, 255))
		screen.blit(hud, (12, 12))
		pygame.display.flip()


if __name__ == "__main__":
	main()
