"""
MuJoCo RGBD Simulation Package

MuJoCoを使ってシーンにカメラを配置してRGB画像を取得するライブラリ
"""

__version__ = "0.1.0"
__author__ = "deankh"

from mujoco_rgbd_sim.geometric_objects import GeometricObject, Box, Cylinder, Mesh
from mujoco_rgbd_sim.mujoco_camera import Camera
from mujoco_rgbd_sim.mujoco_scene_builder import MujocoSceneBuilder
from mujoco_rgbd_sim.mujoco_sim import MujocoSimulation

__all__ = [
    "GeometricObject",
    "Box",
    "Cylinder",
    "Mesh",
    "Camera",
    "MujocoSceneBuilder",
    "MujocoSimulation",
]
