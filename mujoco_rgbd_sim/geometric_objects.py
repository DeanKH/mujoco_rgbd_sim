from typing import Tuple
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class GeometricObject(ABC):
    """Abstract base class for geometric objects in MuJoCo scene"""
    name: str
    position: Tuple[float, float, float] = (0, 0, 0)
    euler: Tuple[float, float, float] = (0, 0, 0)
    color: Tuple[float, float, float, float] = (1, 1, 1, 1)

    @abstractmethod
    def get_geom_type(self) -> str:
        """Return the MuJoCo geometry type"""
        pass

    @abstractmethod
    def get_size_string(self) -> str:
        """Return the size parameter string for MuJoCo"""
        pass

    def to_xml_tree(self) -> ET.Element:
        """Convert object to XML tree element"""
        body_elem = ET.Element(
            "body",
            name=self.name,
            pos=" ".join(map(str, self.position)),
            euler=" ".join(map(str, self.euler)),
        )
        geom_elem = ET.SubElement(
            body_elem,
            "geom",
            name=self.name,
            size=self.get_size_string(),
            type=self.get_geom_type(),
            rgba=" ".join(map(str, self.color)),
        )
        return body_elem


@dataclass
class Box(GeometricObject):
    """Box geometric object"""
    size: Tuple[float, float, float] = (0.1, 0.1, 0.1)

    def get_geom_type(self) -> str:
        return "box"

    def get_size_string(self) -> str:
        return " ".join(map(str, self.size))


@dataclass
class Cylinder(GeometricObject):
    """Cylinder geometric object"""
    radius: float = 0.05
    height: float = 0.1

    def get_geom_type(self) -> str:
        return "cylinder"

    def get_size_string(self) -> str:
        return f"{self.radius} {self.height}"


@dataclass
class Mesh(GeometricObject):
    """Mesh geometric object"""
    mesh_name: str = ""
    scale: Tuple[float, float, float] = (1.0, 1.0, 1.0)

    def get_geom_type(self) -> str:
        return "mesh"

    def get_size_string(self) -> str:
        return " ".join(map(str, self.scale))

    def to_xml_tree(self) -> ET.Element:
        """Convert mesh object to XML tree element"""
        body_elem = ET.Element(
            "body",
            name=self.name,
            pos=" ".join(map(str, self.position)),
            euler=" ".join(map(str, self.euler)),
        )
        geom_elem = ET.SubElement(
            body_elem,
            "geom",
            name=self.name,
            mesh=self.mesh_name,
            type=self.get_geom_type(),
            rgba=" ".join(map(str, self.color)),
        )
        return body_elem