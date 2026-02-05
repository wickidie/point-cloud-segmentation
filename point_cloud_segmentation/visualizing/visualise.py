import matplotlib.pyplot as plt
import open3d as o3d
from open3d.cpu.pybind.visualization import Visualizer, RenderOption

def visualize_geometries(geometries, colors=None, show_normal=False):
    if colors is None:
        colors = plt.get_cmap("gist_rainbow")
    # logger.info(len(pcd.points))
    visualizer: Visualizer = o3d.visualization.Visualizer()
    visualizer.create_window()

    if not isinstance(geometries, list):
        geometries = [geometries]

    for i, geom in enumerate(geometries):
        if hasattr(geom, 'paint_uniform_color'):
            color = colors(i / len(geometries))[:3]
            geom.paint_uniform_color(color)
        visualizer.add_geometry(geom)

    vis_opt: RenderOption = visualizer.get_render_option()
    vis_opt.background_color = (0.3, 0.3, 0.3)
    vis_opt.point_show_normal = show_normal

    visualizer.run()
    visualizer.destroy_window()
