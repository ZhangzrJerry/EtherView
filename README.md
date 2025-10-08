# EtherView

EtherView unveils the unseen dimensions, transforming point clouds and meshes into luminous digital visions.

Lightweight helpers to plot point clouds, triangle meshes and simple pose axes using PyVista.

## Installation

Install directly from GitHub:

```powershell
pip install git+ssh://git@github.com/ZhangzrJerry/EtherView.git
```

If you run into issues with the optional dependencies, install them explicitly:

```powershell
pip install numpy trimesh open3d pyvista
```

## API (short)

- PointCloud(points: np.ndarray, colors: str = '#26D701', point_size: float = 3.0)
- Trimesh(mesh: trimesh.Trimesh, colors: str = '#26D701', ...)
- plot(meshes: list[Trimesh]=[], pcds: list[PointCloud]=[], poses: list=[], window_size=(w,h), save_path=None)

## License

This project is licensed under the terms in the repository `LICENCE` file.
