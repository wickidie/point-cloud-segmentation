import laspy
import numpy as np
import open3d as o3d
from loguru import logger
from laspy import LasData

def las2pcd(file_path: str) -> o3d.geometry.PointCloud:
    """
    Read .las or .laz file and convert it to Open3D point cloud
    :param file_path:
    :return:
    """
    las: LasData = laspy.read(file_path)
    points: np.ndarray = np.vstack((las.x, las.y, las.z)).transpose()
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)

    logger.success(f"PointCloud loaded from: {file_path}")
    logger.info(pcd)
    return pcd

def pcd2las(pcd: o3d.geometry.PointCloud, output_filepath: str, point_format=3, version="1.4"):
    """
    Write Open3D point cloud to .las or .laz file
    :param pcd:
    :param output_filepath:
    :param point_format:
    :param version:
    :return:
    """
    xyz = np.asarray(pcd.points)
    if pcd.has_colors():
        logger.info("Point cloud has colors")
        colors = np.asarray(pcd.colors) * 65535.0
        colors = colors.astype(np.uint16)
    else:
        logger.info("Point cloud doesn`t colors")
        colors = None

    header = laspy.LasHeader(point_format=point_format, version=version)
    header.offsets = np.floor(np.min(xyz, axis=0))
    header.scales = [0.01, 0.01, 0.01]

    las = laspy.LasData(header)
    las.x = xyz[:, 0]
    las.y = xyz[:, 1]
    las.z = xyz[:, 2]

    if colors is not None:
        las.red = colors[:, 0]
        las.green = colors[:, 1]
        las.blue = colors[:, 2]

    las.write(output_filepath)
    logger.success(f"Successfully exported point cloud to {output_filepath}")
