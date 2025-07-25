import mujoco_rgbd_sim.mujoco_scene_builder as sb
import mujoco_rgbd_sim.mujoco_sim as ms
import pprint
import cv2
import numpy as np

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
    cv2.imshow("Captured Image", image)

    # normalize depth
    depth = cv2.normalize(depth, None, 0, 255, cv2.NORM_MINMAX)
    depth = depth.astype(np.uint8)
    cv2.imshow("Depth Image", depth)
    cv2.waitKey(0)
cv2.destroyAllWindows()
