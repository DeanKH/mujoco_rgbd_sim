import xml.etree.ElementTree as ET
from mujoco_rgbd_sim.mujoco_camera import Camera
from mujoco_rgbd_sim.geometric_objects import GeometricObject


class MujocoSceneBuilder:
    def __init__(self):
        self.objects = []
        self.cameras = []

    def set_scene_template_file(self, template_file: str):
        """シーンテンプレートファイルを設定"""
        self.xml_content = ET.parse(template_file).getroot()

        # return this for chaining
        return self

    def set_scene_template_text(self, xml_template: str):
        self.xml_content = ET.fromstring(xml_template)
        return self

    def add_object(self, object: GeometricObject):
        self.objects.append(object)
        return self

    def add_camera(self, camera: Camera):
        self.cameras.append(camera)
        return self

    def build(self) -> str:
        """シーンXMLを構築"""
        worldbody = self.xml_content.find("worldbody")
        if worldbody is None:
            raise ValueError("Worldbody element not found in the XML template.")

        for obj in self.objects:
            worldbody.append(obj.get_worldbody_element())

        for cam in self.cameras:
            worldbody.append(cam.get_worldbody_element())
        ET.indent(self.xml_content)
        return ET.tostring(self.xml_content).decode("utf-8")
