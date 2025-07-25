import mujoco_rgbd_sim.mujoco_scene_builder as sb
import mujoco_rgbd_sim.mujoco_sim as ms
import pprint
import cv2
import numpy as np


def output_as_xyz(filename: str, data: np.ndarray):
    """
    データをXYZ形式でファイルに出力
    Args:
        filename: 出力ファイル名
        data: 出力するデータ (N, 3) の形状を持つnumpy配列
    """
    with open(filename, "w") as f:
        for point in data:
            f.write(f"{point[0]} {point[1]} {point[2]}\n")


ceil_camera = sb.Camera(
    name="ceil_camera0",
    position=(0, 0, 1.5),
    xyaxes=(1, 0, 0, 0, 1, 0),
    fovy=80.0,
    camera_width=1280,
    camera_height=720,
)

hand_camera = sb.Camera(
    name="hand_camera0",
    position=(0, 0, 0.5),
    xyaxes=(1, 0, 0, 0, 1, 0),
    fovy=60.0,
    camera_width=640,
    camera_height=480,
)
box = sb.Box(
    name="box0",
    size=(0.08, 0.06, 0.05),
    position=(0, 0, 0.025),
    color=(0.8, 0.2, 0.2, 1.0),
)

xml_str = (
    sb.MujocoSceneBuilder()
    .set_scene_template_file("empty_scene.xml")
    .add_camera(ceil_camera)
    .add_camera(hand_camera)
    .add_object(box)
    .build()
)

print(xml_str)
with open("output/scene.xml", "w") as f:
    f.write(xml_str)

sim = ms.MujocoSimulation()
sim.setup(xml_str)

for camera in [ceil_camera, hand_camera]:
    print(f"Camera: {camera.name}, Position: {camera.position}, FOVY: {camera.fovy}")
    image, depth = sim.capture_image(camera)
    # normalize depth
    # depth = cv2.normalize(depth, None, 0, 255, cv2.NORM_MINMAX)
    # depth = depth.astype(np.uint8)
    intrinsic = camera.get_camera_matrix()

    data = []
    for y in range(depth.shape[0]):
        for x in range(depth.shape[1]):
            z = depth[y, x]
            if z > 0:  # Skip invalid depth values
                x_world = (x - intrinsic[0, 2]) * z / intrinsic[0, 0]
                y_world = (y - intrinsic[1, 2]) * z / intrinsic[1, 1]
                data.append([x_world, y_world, z])
    data = np.array(data)
    output_as_xyz(f"output/{camera.name}_depth.xyz", data)

    cv2.imshow("Captured Image", image)
    cv2.imshow("Depth Image", depth)
    cv2.waitKey(0)
cv2.destroyAllWindows()
