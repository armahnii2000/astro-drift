# Astro Drift — Unity

The Astro Drift gameplay restated as Unity C# `MonoBehaviour` scripts. Targets **Unity 2022.3 LTS** (also works in 2021.3 LTS+ and Unity 6).

## Open

1. Install [Unity Hub](https://unity.com/download) and **Unity 2022.3 LTS**.
2. In Unity Hub: **Open → Add project from disk**, select this `unity/` directory.
3. On first open, Unity will regenerate `Library/`, `Logs/`, `Temp/`, and generate `.meta` files for each script (all gitignored).
4. Create a new 2D scene, add an empty GameObject and attach `PlayerController` plus a 2D collider/sprite. Add a second empty with `GameManager` and assign the `playerPrefab` / `asteroidPrefab` slots.

## Files

```
Assets/Scripts/
  PlayerController.cs   — input, inertial physics, screen wrap, bullet spawning
  BulletController.cs   — lifetime, screen wrap, asteroid collision via OnTriggerEnter2D
  AsteroidController.cs — drift, spin, size-tier splitting
  GameManager.cs        — wave/score/lives loop
Packages/manifest.json  — UPM dependencies
ProjectSettings/ProjectVersion.txt — editor version pin
```

## Notes

This folder contains only the source-of-truth C# and minimum project metadata. Unity regenerates per-asset `.meta` GUIDs, the `Library/` cache, and binary scene/prefab files on first open — these are intentionally excluded from version control (see the root `.gitignore`).

The Unity bucket on the survey is satisfied by the "or Unity, or Unreal Engine" wording under Open 3D Engine.
