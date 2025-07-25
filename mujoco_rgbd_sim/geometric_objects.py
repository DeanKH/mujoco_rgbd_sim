from typing import Tuple, Optional
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class GeometricObject(ABC):
    """Abstract base class for geometric objects in MuJoCo scene"""

    name: str
    position: Tuple[float, float, float] = (0, 0, 0)
    euler: Optional[Tuple[float, float, float]] = None
    quat: Optional[Tuple[float, float, float, float]] = None  # w, x, y, z
    color: Tuple[float, float, float, float] = (1, 1, 1, 1)

    def __post_init__(self):
        """Validate that either euler or quat is provided, not both"""
        if self.euler is not None and self.quat is not None:
            raise ValueError("Cannot specify both euler and quat. Choose one.")
        if self.euler is None and self.quat is None:
            self.euler = (0, 0, 0)  # Default to zero euler angles

    @abstractmethod
    def get_geom_type(self) -> str:
        """Return the MuJoCo geometry type"""
        pass

    @abstractmethod
    def get_size_string(self) -> str:
        """Return the size parameter string for MuJoCo"""
        pass

    def get_worldbody_element(self) -> ET.Element:
        """Convert object to XML tree element"""
        body_attrs = {
            "name": self.name,
            "pos": " ".join(map(str, self.position)),
        }

        # Add orientation: either euler or quat
        if self.euler is not None:
            body_attrs["euler"] = " ".join(map(str, self.euler))
        elif self.quat is not None:
            body_attrs["quat"] = " ".join(map(str, self.quat))

        body_elem = ET.Element("body", **body_attrs)
        ET.SubElement(
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

    def get_worldbody_element(self) -> ET.Element:
        """Convert mesh object to XML tree element"""
        body_attrs = {
            "name": self.name,
            "pos": " ".join(map(str, self.position)),
        }

        # Add orientation: either euler or quat
        if self.euler is not None:
            body_attrs["euler"] = " ".join(map(str, self.euler))
        elif self.quat is not None:
            body_attrs["quat"] = " ".join(map(str, self.quat))

        body_elem = ET.Element("body", **body_attrs)
        ET.SubElement(
            body_elem,
            "geom",
            name=self.name,
            mesh=self.mesh_name,
            type=self.get_geom_type(),
            rgba=" ".join(map(str, self.color)),
        )
        return body_elem
