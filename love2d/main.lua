-- Astro Drift — Love 2D
-- Inertial drifting ship with screen wrap. Mirrors the Godot version's feel.

local W, H = 960, 540
local THRUST = 350
local ROT_SPEED = 4
local DRAG_PER_SEC = 0.55
local MAX_SPEED = 480

local ship = { x = W / 2, y = H / 2, vx = 0, vy = 0, rot = 0 }
local bullets = {}
local stars = {}
local cooldown = 0
local BULLET_SPEED = 700
local BULLET_LIFE = 1.0

local function len(x, y) return math.sqrt(x * x + y * y) end

function love.load()
	love.graphics.setBackgroundColor(0.04, 0.05, 0.09)
	love.window.setTitle("Astro Drift — Love 2D")
	math.randomseed(os.time())
	for i = 1, 80 do
		stars[i] = { x = math.random() * W, y = math.random() * H, b = 0.3 + math.random() * 0.7 }
	end
end

local function wrap(o, w, h, pad)
	pad = pad or 20
	if o.x < -pad then o.x = w + pad end
	if o.x > w + pad then o.x = -pad end
	if o.y < -pad then o.y = h + pad end
	if o.y > h + pad then o.y = -pad end
end

function love.update(dt)
	if love.keyboard.isDown("a", "left") then ship.rot = ship.rot - ROT_SPEED * dt end
	if love.keyboard.isDown("d", "right") then ship.rot = ship.rot + ROT_SPEED * dt end

	local thrusting = love.keyboard.isDown("w", "up")
	if thrusting then
		ship.vx = ship.vx + math.cos(ship.rot - math.pi / 2) * THRUST * dt
		ship.vy = ship.vy + math.sin(ship.rot - math.pi / 2) * THRUST * dt
	end
	local damping = DRAG_PER_SEC ^ dt
	ship.vx, ship.vy = ship.vx * damping, ship.vy * damping
	local sp = len(ship.vx, ship.vy)
	if sp > MAX_SPEED then
		ship.vx, ship.vy = ship.vx / sp * MAX_SPEED, ship.vy / sp * MAX_SPEED
	end
	ship.x, ship.y = ship.x + ship.vx * dt, ship.y + ship.vy * dt
	wrap(ship, W, H)

	cooldown = cooldown - dt
	if (love.keyboard.isDown("space") or love.keyboard.isDown("j")) and cooldown <= 0 then
		cooldown = 0.18
		local dx, dy = math.cos(ship.rot - math.pi / 2), math.sin(ship.rot - math.pi / 2)
		table.insert(bullets, { x = ship.x + dx * 18, y = ship.y + dy * 18, vx = dx * BULLET_SPEED, vy = dy * BULLET_SPEED, life = BULLET_LIFE })
	end

	for i = #bullets, 1, -1 do
		local b = bullets[i]
		b.x, b.y = b.x + b.vx * dt, b.y + b.vy * dt
		b.life = b.life - dt
		wrap(b, W, H, 4)
		if b.life <= 0 then table.remove(bullets, i) end
	end
end

local function draw_ship()
	love.graphics.push()
	love.graphics.translate(ship.x, ship.y)
	love.graphics.rotate(ship.rot)
	love.graphics.setColor(0.9, 0.95, 1.0)
	love.graphics.polygon("fill", 0, -14, 10, 12, 0, 6, -10, 12)
	love.graphics.setColor(0.55, 0.75, 1.0)
	love.graphics.setLineWidth(1.5)
	love.graphics.polygon("line", 0, -14, 10, 12, 0, 6, -10, 12)
	if love.keyboard.isDown("w", "up") then
		love.graphics.setColor(1.0, 0.6, 0.2)
		love.graphics.polygon("fill", -5, 8, 0, 18 + math.random() * 6, 5, 8)
	end
	love.graphics.pop()
end

function love.draw()
	for _, s in ipairs(stars) do
		love.graphics.setColor(s.b, s.b, s.b)
		love.graphics.points(s.x, s.y)
	end
	love.graphics.setColor(1.0, 0.95, 0.55)
	for _, b in ipairs(bullets) do
		love.graphics.circle("fill", b.x, b.y, 3)
	end
	draw_ship()
	love.graphics.setColor(0.85, 0.9, 1.0)
	love.graphics.print("Astro Drift — Love 2D  |  WASD/arrows fly, Space fires, Esc quits", 12, 12)
end

function love.keypressed(k)
	if k == "escape" then love.event.quit() end
end
