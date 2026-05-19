# Astro Drift

A small 2D arcade shooter built in **Godot 4.6** with GDScript. Inspired by the Atari classic *Asteroids*: pilot a drifting ship through a screen-wrapping field of asteroids, blast them into smaller pieces, and survive as many waves as you can.

## Demo

![gameplay](docs/demo.gif)

## Controls

| Action | Keys |
|---|---|
| Rotate | `A` / `D` or `Left` / `Right` |
| Thrust | `W` or `Up` |
| Fire | `Space` or `J` |
| Restart (after Game Over) | `R` |

## Features

- Newtonian-style inertial movement with directional thrust and drag
- Screen wrapping for player, bullets, and asteroids
- Three asteroid size tiers that split on hit
- Wave progression with increasing density
- Lives, score, post-death invulnerability, and a game-over flow
- All visuals rendered procedurally via `_draw()` — no external assets

## Project layout

```
astro-drift/
├── project.godot          # Engine config + window/render settings
├── icon.svg               # App icon
├── scenes/
│   └── Main.tscn          # Entry scene
└── scripts/
    ├── Main.gd            # Game manager: waves, lives, score, input
    ├── Player.gd          # Ship: input, physics, shooting
    ├── Bullet.gd          # Projectile + bullet-asteroid collision
    ├── Asteroid.gd        # Drifting asteroid + procedural shape
    └── HUD.gd             # Score / lives / banner UI
```

## Building

Open the project folder in Godot 4.6+ and press `F5`, or run from the command line:

```sh
godot --path .
```

To export a Windows build, configure an Export Preset in *Project → Export* and export to `exports/`.

## Notes

This was built as a self-contained portfolio piece to demonstrate Godot fundamentals: scene tree composition, `Area2D` overlap detection, custom `_draw()` rendering, signal-based decoupling between nodes, and resolution-independent screen wrapping.
