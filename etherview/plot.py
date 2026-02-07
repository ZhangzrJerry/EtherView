import pyvista as pv
from .type import PointCloud, Trimesh, Poses, Line


def plot(
    meshes: list[Trimesh] = [],
    pcds: list[PointCloud] = [],
    poses: list[Poses] = [],
    lines: list[Line] = [],
    window_size: tuple = (2000, 2000),
    save_path: str = None,  # type: ignore
) -> None:
    """
    Plot meshes, point clouds, poses and lines using PyVista.

    Args:
        meshes (list[Trimesh]): List of Trimesh objects.
        pcds (list[PointCloud]): List of PointCloud objects.
        poses (list[Poses]): List of Poses objects.
        lines (list[Line]): List of Line objects.
        window_size (tuple): Size of the plotting window (width, height).
    """
    plotter = pv.Plotter(window_size=window_size, off_screen=True)

    for mesh in meshes:
        pv_mesh = pv.wrap(mesh.mesh)
        pv_args = dict(
            color=mesh.colors,
            ambient=mesh.ambient,
            opacity=mesh.opacity,
            smooth_shading=mesh.smooth_shading,
            specular=mesh.specular,
            show_scalar_bar=False,
            render=False,
        )
        plotter.add_mesh(pv_mesh, **pv_args)  # pyright: ignore[reportArgumentType]

    for pcd in pcds:
        pv_pcd = pv.PolyData(pcd.points)
        plotter.add_points(
            pv_pcd,
            render_points_as_spheres=True,
            color=pcd.colors,
            point_size=pcd.point_size,
            render=False,
            show_scalar_bar=False,
        )

    for pose in poses:
        center, quivers, colors, names = pose.wrap()
        for q, c, n in zip(quivers, colors, names):
            plotter.add_arrows(
                center,
                q,
                color=c,
                scale=pose.quiver_size,
                opacity=pose.opacity,
                name=n,
                show_scalar_bar=False,
                render=False,
            )

    for line in lines:
        if len(line.points) > 1:
            pv_line = pv.lines_from_points(line.points)
            plotter.add_mesh(
                pv_line,
                color=line.color,
                line_width=line.line_width,
                render=False,
                show_scalar_bar=False,
            )

    plotter.render()

    if save_path:
        plotter.show(screenshot=save_path)  # type: ignore
    else:
        plotter.show()

    plotter.close()
    pv.close_all()
