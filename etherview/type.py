from dataclasses import dataclass
import numpy as np
import open3d as o3d
import trimesh
import pyvista as pv
from typing import Tuple
from scipy.spatial.transform import Rotation as R


@dataclass
class Line:
    points: np.ndarray
    color: str = "black"
    line_width: float = 2.0

    @classmethod
    def from_points(cls, points: np.ndarray, color: str = "black", line_width: float = 2.0) -> "Line":
        return cls(points=points, color=color, line_width=line_width)


@dataclass
class PointCloud:
    points: np.ndarray
    colors: str = "#26D701"
    point_size: float = 2.0

    @classmethod
    def from_pointcloud(cls, pcd: o3d.geometry.PointCloud) -> "PointCloud":
        return cls(points=np.asarray(pcd.points))

    @classmethod
    def from_file(cls, pcd_path: str, colors: tuple) -> "PointCloud":
        pcd = o3d.io.read_point_cloud(pcd_path)
        return cls(points=np.asarray(pcd.points))


@dataclass
class Trimesh:
    mesh: trimesh.Trimesh
    colors: str = "grey"
    ambient: float = 0.6
    opacity: float = 0.5
    smooth_shading: bool = True
    specular: float = 1.0

    @classmethod
    def from_triangle_mesh(cls, mesh: o3d.geometry.TriangleMesh) -> "Trimesh":
        return cls(
            mesh=trimesh.Trimesh(
                # vertices=np.asarray(mesh.vertices),
                # faces=np.asarray(mesh.triangles),
            )
        )

    @classmethod
    def from_file(cls, mesh_path: str) -> "Trimesh":
        mesh = trimesh.load_mesh(mesh_path)
        return cls(mesh=mesh)


class Poses:
    poses: np.ndarray
    opacity: float = 1.0
    quiver_size: float = 0.1

    def wrap(self) -> Tuple[np.ndarray, list, list, list]:
        """
        Wrap the poses into a PyVista PolyData object with quivers representing the orientation.

        Returns:
            Tuple containing:
            - centers: (N, 3) array of pose centers (x, y, z)
            - quivers: List of vectors for x, y, z axes
            - colors: List of colors for each axis
            - names: List of names for each axis
        """
        quivers = pv.PolyData(self.poses[:, :3, 3])  # (N, 3) [x, y, z]
        x, y, z = np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 1])
        r = R.from_matrix(self.poses[:, 0:3, 0:3])  # (N, 3, 3)
        quivers["xvectors"], quivers["yvectors"], quivers["zvectors"] = (
            r.apply(x) * self.quiver_size,
            r.apply(y) * self.quiver_size,
            r.apply(z) * self.quiver_size,
        )
        return (
            self.poses[:, :3, 3],
            [quivers["xvectors"]] + [quivers["yvectors"]] + [quivers["zvectors"]],
            ["r", "g", "b"],
            ["xvectors", "yvectors", "zvectors"],
        )
