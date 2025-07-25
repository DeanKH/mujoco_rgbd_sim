import numpy as np
import mujoco
from typing import Tuple
from mujoco_rgbd_sim.mujoco_camera import Camera


class MujocoSimulation:
    def __init__(self):
        self.model = None
        self.data = None
        self.renderer = None
        self.render_size = (640, 480)

    def setup(self, scene_xml_str: str):
        self.model = mujoco.MjModel.from_xml_string(scene_xml_str)
        self.data = mujoco.MjData(self.model)
        # MjRenderContextOffscreen
        self.renderer = mujoco.Renderer(self.model)
        mujoco.mj_step(self.model, self.data)

    def capture_image(self, camera: Camera) -> Tuple[np.ndarray, np.ndarray]:
        if self.model is None or self.data is None:
            raise ValueError(
                "シミュレーションが初期化されていません。setup_simulation()を先に呼び出してください。"
            )
        camera_id = mujoco.mj_name2id(
            self.model, mujoco.mjtObj.mjOBJ_CAMERA, camera.name
        )
        if camera_id == -1:
            raise ValueError(f"カメラ '{camera.name}' が見つかりません")

        renderer = camera.get_renderer(self.model)
        renderer.update_scene(self.data, camera=camera_id)

        rgb_image = renderer.render()

        renderer.enable_depth_rendering()
        renderer.update_scene(self.data, camera=camera_id)
        depth = renderer.render()
        renderer.disable_depth_rendering()

        min_depth = depth.min()
        max_depth = depth.max()
        print(f"Depth min: {min_depth}, max: {max_depth}")

        depth *= camera.depth_factor
        # type change to uint16 for depth
        depth = depth.astype(np.uint16)

        return rgb_image, depth
