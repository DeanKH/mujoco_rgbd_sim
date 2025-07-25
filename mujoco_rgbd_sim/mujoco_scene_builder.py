import numpy as np
import mujoco
import cv2
import matplotlib.pyplot as plt
import matplotlib
from typing import Tuple, Optional
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from mujoco_rgbd_sim.mujoco_camera import Camera


@dataclass
class Box:
    name: str
    size: Tuple[float, float, float]
    position: Tuple[float, float, float] = (0, 0, 0)
    euler: Tuple[float, float, float] = (0, 0, 0)
    color: Tuple[float, float, float] = (1, 1, 1, 1)

    def to_xml_tree(self) -> ET.Element:
        box_elem = ET.Element(
            "body",
            name=self.name,
            pos=" ".join(map(str, self.position)),
            euler=" ".join(map(str, self.euler)),
        )
        geom_elem = ET.SubElement(
            box_elem,
            "geom",
            name=self.name,
            size=" ".join(map(str, self.size)),
            type="box",
            rgba=" ".join(map(str, self.color)),
        )
        return box_elem


@dataclass
class Cylinder:
    name: str
    radius: float
    height: float
    position: Tuple[float, float, float] = (0, 0, 0)
    euler: Tuple[float, float, float] = (0, 0, 0)
    color: Tuple[float, float, float] = (1, 1, 1, 1)

    def to_xml_tree(self) -> ET.Element:
        cylinder_elem = ET.Element(
            "body",
            name=self.name,
            pos=" ".join(map(str, self.position)),
            euler=" ".join(map(str, self.euler)),
        )
        geom_elem = ET.SubElement(
            cylinder_elem,
            "geom",
            name=self.name,
            size=f"{self.radius} {self.height}",
            type="cylinder",
            rgba=" ".join(map(str, self.color)),
        )
        return cylinder_elem


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

    def add_object(self, object: Box | Cylinder):
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
            worldbody.append(obj.to_xml_tree())

        for cam in self.cameras:
            worldbody.append(cam.to_xml_tree())
        ET.indent(self.xml_content)
        return ET.tostring(self.xml_content).decode("utf-8")
