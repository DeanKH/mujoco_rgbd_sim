# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a MuJoCo-based RGBD camera simulation library that allows you to:
- Create virtual scenes with cameras and objects
- Capture RGB and depth images from multiple cameras
- Convert depth data to 3D point clouds

The library uses MuJoCo physics engine for simulation and OpenCV for image processing.

## Development Environment

This project uses `uv` as the package manager. The Python dependencies are managed in `pyproject.toml`.

### Common Commands

```bash
# Install dependencies (including dev dependencies)
uv sync

# Run the example simulation
uv run python example/simple_camera.py

# Install in development mode
uv pip install -e .
```

## Architecture

### Core Modules

1. **mujoco_scene_builder.py**: Scene construction API
   - `MujocoSceneBuilder`: Main builder class for creating MuJoCo XML scenes
   - `Camera`: Camera configuration dataclass with intrinsic parameter calculation
   - Object classes: `Box`, `Cylinder`, etc. for adding objects to scenes

2. **mujoco_sim.py**: Simulation engine
   - `MujocoSimulation`: Handles MuJoCo model loading and image capture
   - Manages RGB and depth rendering through MuJoCo's renderer

3. **mujoco_camera.py**: Camera utilities
   - Camera intrinsic matrix calculation
   - Depth factor management for depth-to-metric conversion

### Typical Workflow

1. Create cameras and objects using the builder classes
2. Use `MujocoSceneBuilder` to compose them into a scene XML
3. Initialize `MujocoSimulation` with the XML
4. Capture RGB/depth images from cameras
5. Process depth data (e.g., convert to point clouds)

### Key Technical Details

- Camera intrinsic matrix calculation is in `Camera.get_camera_matrix()`
- Depth values are scaled by `camera.depth_factor` (default 1000.0)
- Scene templates are loaded from XML files (e.g., `empty_scene.xml`)
- Output format supports XYZ point cloud export