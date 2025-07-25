import numpy as np
import mujoco
import cv2
import matplotlib.pyplot as plt
import matplotlib
from typing import Tuple, Optional
import xml.etree.ElementTree as ET
from dataclasses import dataclass


class Camera:
    def __init__(
        self,
        name: str,
        position: Tuple[float, float, float],
        fovy: float = 45.0,
        xyaxes: Tuple[float, float, float, float, float, float] = (1, 0, 0, 0, 1, 0),
        camera_width: int = 640,
        camera_height: int = 480,
    ):
        """
        カメラの初期化

        Args:
            name: カメラの名前
            position: カメラの位置 (x, y, z)
            fovy: 垂直視野角 (degrees)
        """
        self.name = name
        self.position = position
        self.fovy = fovy
        self.xyaxes = xyaxes
        self.camera_width = camera_width
        self.camera_height = camera_height
        self.renderer = None

    def get_renderer(self, model: mujoco.MjModel) -> mujoco.Renderer:
        """レンダラーを取得"""
        if self.renderer is None:
            self.renderer = mujoco.Renderer(
                model, self.camera_height, self.camera_width
            )
        return self.renderer

    def to_xml_tree(self) -> ET.Element:
        camera_elem = ET.Element(
            "camera",
            name=self.name,
            pos=" ".join(map(str, self.position)),
            fovy=str(self.fovy),
            xyaxes=" ".join(map(str, self.xyaxes)),
        )
        return camera_elem
