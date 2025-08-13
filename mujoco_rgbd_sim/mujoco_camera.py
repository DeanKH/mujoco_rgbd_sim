import numpy as np
import mujoco
from typing import Tuple
import xml.etree.ElementTree as ET
import math
import transforms3d as t3d


class Camera:
    def __init__(
        self,
        name: str,
        position: Tuple[float, float, float],
        fovy: float = 45.0,
        quat: Tuple[float, float, float, float] = (1.0, 0.0, 0.0, 0.0),
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
        self.quat = quat

        tf_camera_base_to_optical = t3d.quaternions.axangle2quat([1, 0, 0], np.pi)

        q = np.array([quat[0], quat[1], quat[2], quat[3]])
        self.tf_world_to_base = t3d.quaternions.qmult(
            q, t3d.quaternions.qinverse(tf_camera_base_to_optical)
        )

        self.camera_width = camera_width
        self.camera_height = camera_height
        self.renderer = None
        self.depth_factor = 1000.0

    def get_renderer(self, model: mujoco.MjModel) -> mujoco.Renderer:
        """レンダラーを取得"""
        if self.renderer is None:
            self.renderer = mujoco.Renderer(
                model, self.camera_height, self.camera_width
            )
        return self.renderer

    def get_worldbody_element(self) -> ET.Element:
        camera_elem = ET.Element(
            "camera",
            name=self.name,
            pos=" ".join(map(str, self.position)),
            fovy=str(self.fovy),
            quat=" ".join(map(str, self.tf_world_to_base)),
        )
        return camera_elem

    def compute_camera_intrinsics(self):
        """
        MujocoのCameraパラメータから内部行列(fx, fy, cx, cy)を計算する

        Args:
            camera: Camera object with fovy, camera_width, camera_height attributes

        Returns:
            tuple: (fx, fy, cx, cy)
        """
        camera = self

        # 画像の中心座標 (cx, cy)
        cx = camera.camera_width / 2.0
        cy = camera.camera_height / 2.0

        # FOVYから焦点距離を計算
        # fy = height / (2 * tan(fovy/2))
        fovy_rad = math.radians(camera.fovy)
        fy = camera.camera_height / (2 * math.tan(fovy_rad / 2.0))

        # アスペクト比から fovx を計算し、fx を求める
        aspect_ratio = camera.camera_width / camera.camera_height
        fovx_rad = 2.0 * math.atan(aspect_ratio * math.tan(fovy_rad / 2.0))
        fx = camera.camera_width / (2 * math.tan(fovx_rad / 2.0))

        return fx, fy, cx, cy

    def get_camera_matrix(self):
        """
        内部行列をOpenCV形式の3x3行列として取得

        Args:
            camera: Camera object

        Returns:
            numpy.ndarray: 3x3 camera matrix
        """
        fx, fy, cx, cy = self.compute_camera_intrinsics()

        camera_matrix = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])

        return camera_matrix
