"""Module for mapping panel pixels to animation pixels."""

import numpy as np
from collections import OrderedDict
import cv2

# Pixel mapping from pixel_map_helper.py in touch_dome


PIXEL_MAP_SMOL = np.array([
    [963, 45], [965, 106], [1032, 171], [966, 171], [901, 171], [904, 237],
    [967, 237], [1030, 237], [1094, 302], [1029, 302], [964, 302], [899, 301],
    [834, 301], [773, 364], [838, 364], [902, 364], [967, 364], [1032, 365],
    [1096, 365], [1161, 365], [1224, 429], [1159, 429], [1095, 429],
    [1030, 429], [966, 429], [901, 429], [836, 429], [772, 429], [707, 429],
    [706, 494], [771, 494], [836, 494], [900, 494], [965, 494], [1030, 494],
    [1094, 494], [1159, 494], [1224, 494], [1287, 559], [1222, 559],
    [1158, 559], [1093, 559], [1028, 559], [964, 559], [899, 559], [834, 559],
    [769, 559], [705, 559], [640, 559], [579, 623], [643, 623], [708, 623],
    [772, 624], [836, 624], [901, 624], [965, 624], [1029, 624], [1094, 624],
    [1158, 624], [1222, 625], [1287, 625], [1351, 625], [1353, 690],
    [1288, 690], [1224, 690], [1159, 690], [1095, 690], [1030, 690], [966, 690],
    [901, 689], [836, 689], [772, 689], [707, 689], [643, 689], [578, 689],
    [514, 753], [578, 753], [643, 753], [707, 754], [772, 754], [836, 754],
    [901, 754], [965, 754], [1029, 755], [1094, 755], [1158, 755], [1223, 755],
    [1287, 756], [1352, 756], [1416, 756], [1483, 818], [1418, 818],
    [1354, 818], [1289, 817], [1224, 817], [1160, 817], [1095, 816],
    [1031, 816], [966, 816], [901, 816], [837, 816], [772, 815],
    [708, 815], [643, 815], [578, 814], [514, 814], [449, 814],
    [449, 881], [514, 881], [578, 881], [643, 881], [708, 881],
    [772, 881], [837, 881], [901, 881], [966, 881], [1031, 881],
    [1095, 881], [1160, 881], [1224, 881], [1289, 881], [1354, 881],
    [1418, 881], [1483, 881], [1546, 949], [1482, 949], [1417, 949],
    [1352, 949], [1288, 949], [1224, 949], [1159, 949], [1094, 949],
    [1030, 949], [966, 948], [901, 948], [836, 948], [772, 948],
    [708, 948], [643, 948], [578, 948], [514, 948], [450, 948],
    [385, 948], [323, 1009], [387, 1009], [452, 1009], [516, 1009],
    [580, 1010], [645, 1010], [709, 1010], [773, 1010], [838, 1010],
    [902, 1010], [966, 1010], [1031, 1011], [1095, 1011], [1160, 1011],
    [1224, 1011], [1288, 1011], [1353, 1011], [1417, 1012], [1481, 1012],
    [1546, 1012], [1610, 1012], [1613, 1079], [1548, 1079], [1484, 1078],
    [1419, 1078], [1354, 1078], [1290, 1078], [1225, 1078], [1160, 1077],
    [1095, 1077], [1031, 1077], [966, 1076], [901, 1076], [837, 1076],
    [772, 1076], [707, 1076], [642, 1075], [578, 1075], [513, 1075],
    [448, 1074], [384, 1074], [319, 1074], [256, 1139], [320, 1139],
    [385, 1139], [450, 1139], [514, 1138], [578, 1138], [643, 1138],
    [708, 1138], [772, 1138], [836, 1138], [901, 1138], [966, 1138],
    [1030, 1137], [1094, 1137], [1159, 1137], [1224, 1137], [1288, 1137],
    [1352, 1137], [1417, 1137], [1482, 1136], [1546, 1136], [1610, 1136],
    [1675, 1136], [1739, 1202], [1675, 1202], [1610, 1202], [1546, 1202],
    [1481, 1202], [1417, 1202], [1352, 1202], [1288, 1202], [1223, 1202],
    [1159, 1202], [1094, 1202], [1030, 1202], [966, 1202], [901, 1203],
    [837, 1203], [772, 1203], [708, 1203], [643, 1203], [579, 1203],
    [514, 1203], [450, 1203], [385, 1203], [321, 1203], [256, 1203],
    [192, 1203], [128, 1267], [192, 1267], [257, 1267], [321, 1267],
    [386, 1267], [450, 1267], [515, 1267], [579, 1267], [643, 1267],
    [708, 1267], [772, 1267], [837, 1267], [901, 1267], [966, 1266],
    [1030, 1266], [1094, 1266], [1159, 1266], [1223, 1266], [1288, 1266],
    [1352, 1266], [1416, 1266], [1481, 1266], [1545, 1266], [1610, 1266],
    [1674, 1266], [1739, 1266], [1803, 1266]
])

PIXEL_MAP_BIG = np.array([
    [1374, 66], [1374, 157], [1460, 239], [1374, 242], [1289, 244],
    [1287, 333], [1375, 333], [1463, 333], [1547, 410], [1460, 411],
    [1374, 412], [1288, 414], [1201, 415], [1201, 499], [1288, 500],
    [1375, 502], [1462, 503], [1549, 504], [1634, 588], [1548, 588],
    [1461, 587], [1375, 587], [1289, 587], [1202, 586], [1116, 586],
    [1116, 669], [1202, 670], [1289, 670], [1375, 671], [1461, 672],
    [1548, 672], [1634, 673], [1725, 760], [1638, 760], [1551, 760],
    [1464, 759], [1377, 759], [1290, 759], [1203, 758], [1116, 758],
    [1029, 758], [940, 843], [1027, 844], [1113, 844], [1200, 845],
    [1286, 845], [1373, 846], [1460, 847], [1546, 847], [1633, 848],
    [1719, 848], [1806, 849], [1808, 930], [1721, 930], [1635, 930],
    [1548, 930], [1462, 930], [1375, 930], [1288, 930], [1202, 930],
    [1115, 930], [1029, 930], [942, 930], [857, 1015], [943, 1015],
    [1029, 1015], [1116, 1016], [1202, 1016], [1288, 1016], [1374, 1016],
    [1460, 1016], [1546, 1016], [1632, 1016], [1719, 1017], [1805, 1017],
    [1891, 1017], [1895, 1110], [1808, 1110], [1722, 1109], [1635, 1109],
    [1548, 1109], [1462, 1108], [1375, 1108], [1288, 1108], [1202, 1107],
    [1115, 1107], [1028, 1107], [942, 1106], [855, 1106], [770, 1191],
    [856, 1191], [943, 1191], [1029, 1191], [1116, 1191], [1202, 1191],
    [1289, 1191], [1375, 1191], [1461, 1191], [1548, 1191], [1634, 1191],
    [1721, 1191], [1807, 1191], [1894, 1191], [1980, 1191], [1982, 1278],
    [1896, 1278], [1809, 1278], [1723, 1278], [1636, 1278], [1550, 1278],
    [1463, 1278], [1377, 1278], [1291, 1278], [1204, 1278], [1118, 1278],
    [1031, 1278], [945, 1278], [858, 1278], [772, 1278], [685, 1361],
    [772, 1361], [858, 1361], [944, 1361], [1031, 1362], [1118, 1362],
    [1204, 1362], [1290, 1362], [1377, 1362], [1464, 1362], [1550, 1362],
    [1636, 1362], [1723, 1362], [1810, 1363], [1896, 1363], [1982, 1363],
    [2069, 1363], [2154, 1450], [2067, 1450], [1981, 1450], [1894, 1450],
    [1808, 1450], [1721, 1450], [1634, 1450], [1548, 1450], [1461, 1450],
    [1374, 1450], [1288, 1450], [1201, 1450], [1115, 1450], [1028, 1450],
    [941, 1450], [855, 1450], [768, 1450], [682, 1450], [595, 1450],
    [596, 1537], [682, 1537], [768, 1537], [854, 1536], [940, 1536],
    [1026, 1536], [1112, 1536], [1198, 1535], [1284, 1535], [1370, 1535],
    [1456, 1535], [1542, 1535], [1628, 1534], [1714, 1534], [1800, 1534],
    [1886, 1534], [1972, 1533], [2058, 1533], [2144, 1533], [2237, 1621],
    [2151, 1621], [2065, 1621], [1979, 1621], [1893, 1621], [1806, 1621],
    [1720, 1621], [1634, 1621], [1548, 1621], [1462, 1621], [1376, 1621],
    [1290, 1621], [1204, 1621], [1118, 1621], [1032, 1621], [946, 1621],
    [859, 1621], [773, 1621], [687, 1621], [601, 1621], [515, 1621],
    [513, 1706], [599, 1706], [686, 1706], [772, 1706], [858, 1706],
    [944, 1706], [1031, 1705], [1117, 1705], [1203, 1705], [1290, 1705],
    [1376, 1705], [1462, 1705], [1549, 1705], [1635, 1705], [1721, 1705],
    [1808, 1704], [1894, 1704], [1980, 1704], [2066, 1704], [2153, 1704],
    [2239, 1704], [2324, 1795], [2238, 1795], [2152, 1795], [2065, 1795],
    [1979, 1795], [1893, 1795], [1807, 1795], [1721, 1795], [1635, 1795],
    [1548, 1795], [1462, 1795], [1376, 1795], [1290, 1795], [1204, 1795],
    [1117, 1795], [1031, 1795], [945, 1795], [859, 1795], [773, 1795],
    [687, 1795], [600, 1795], [514, 1795], [428, 1795], [341, 1882],
    [427, 1882], [513, 1882], [600, 1882], [686, 1882], [772, 1882],
    [858, 1882], [944, 1881], [1030, 1881], [1116, 1881], [1203, 1881],
    [1289, 1881], [1375, 1881], [1461, 1881], [1547, 1881], [1634, 1881],
    [1720, 1881], [1806, 1881], [1892, 1880], [1978, 1880], [2064, 1880],
    [2150, 1880], [2237, 1880], [2323, 1880], [2409, 1880], [2409, 1967],
    [2323, 1967], [2237, 1967], [2150, 1967], [2064, 1967], [1978, 1967],
    [1892, 1967], [1806, 1967], [1719, 1967], [1633, 1967], [1547, 1967],
    [1461, 1967], [1374, 1967], [1288, 1967], [1202, 1967], [1116, 1967],
    [1030, 1967], [943, 1967], [857, 1967], [771, 1967], [685, 1967],
    [599, 1967], [512, 1967], [426, 1967], [340, 1967], [255, 2052],
    [341, 2052], [427, 2052], [513, 2052], [599, 2052], [686, 2052],
    [772, 2052], [858, 2051], [944, 2051], [1030, 2051], [1116, 2051],
    [1202, 2051], [1288, 2051], [1374, 2051], [1461, 2051], [1547, 2051],
    [1633, 2051], [1719, 2051], [1805, 2051], [1891, 2051], [1977, 2050],
    [2063, 2050], [2150, 2050], [2236, 2050], [2322, 2050], [2408, 2050],
    [2494, 2050]
])


def normalize_pix_map(pix_map):
    """Return a normalized copy of `pixel map` all x, y between 0, 1."""
    normalized = pix_map.astype(np.float64)

    pix_min_x = normalized.min(0)[0]
    pix_max_x = normalized.max(0)[0]
    pix_min_y = normalized.min(1)[0]
    pix_max_y = normalized.max(1)[0]
    pix_breadth_x = pix_max_x - pix_min_x
    pix_breadth_y = pix_max_y - pix_min_y
    pix_breadth_max = max(pix_breadth_x, pix_breadth_y)

    # logging.debug(
    #     "mins: (%4d, %4d), maxs: (%4d, %4d), breadth: (%4d, %4d)" % (
    #         pix_min_x, pix_min_y, pix_max_x, pix_max_y,
    #         pix_breadth_x, pix_breadth_y
    #     )
    # )

    normalized[..., [0, 1]] -= [pix_min_x, pix_min_y]
    normalized *= (1 / pix_breadth_max)

    # TODO: probably need to centre this better

    return normalized


def mat_rotation_2d(angle):
    """
    Generate a rotation matrix from the angle in degrees.
    """
    theta = np.radians(angle)
    val_cos, val_sin = np.cos(theta), np.sin(theta)
    return np.matrix([[val_cos, -val_sin], [val_sin, val_cos]])


def vector_transform(vector, matrix):
    # TODO: fix this math
    return np.asarray(matrix * np.asmatrix(vector).transpose()).transpose()[0]


def rotate_vector(vector, angle):
    mat = mat_rotation_2d(angle)
    return vector_transform(vector, mat)


def scale_mapping(mapping, scalar):
    return [
        scalar * coordinate \
        for coordinate in mapping
    ]


def transpose_mapping(mapping, offset):
    return [
        coordinate + offset \
        for coordinate in mapping
    ]


def rotate_mapping(mapping, angle):
    mat = mat_rotation_2d(angle)
    return [
        vector_transform(coordinate, mat)
        for coordinate in mapping
    ]


PANELS = OrderedDict([
    (0, [
        # (0, 'big'),
        (1, 'smol', 0.5, (1 * 360 / 5), rotate_vector((0, 0.265), (1 * 360 / 5))),
        # (2, 'smol'),
        # (3, 'smol')
    ]),
    (1, [
        # (0, 'big'),
        (1, 'smol', 0.5, (2 * 360 / 5), rotate_vector((0, 0.265), (2 * 360 / 5))),
        # (2, 'smol'),
        # (3, 'smol')
    ]),
    (2, [
        # (0, 'big'),
        (1, 'smol', 0.5, (3 * 360 / 5), rotate_vector((0, 0.265), (3 * 360 / 5))),
        # (2, 'smol'),
        # (3, 'smol')
    ]),
    (3, [
        # (0, 'big'),
        (1, 'smol', 0.5, (4 * 360 / 5), rotate_vector((0, 0.265), (4 * 360 / 5))),
        # (2, 'smol'),
        # (3, 'smol')
    ]),
    (4, [
        # (0, 'big', 0.5, -(4 * 360 / 5), rotate_vector((0, 0.265), (4 * 360 / 5))),
        (1, 'smol', 0.5, (0 * 360 / 5), rotate_vector((0, 0.265), (0 * 360 / 5))),
        # (2, 'smol'),
        # (3, 'smol')
    ])
])


def draw_map(image, pix_map_normlized, radius=1, outline=None):
    """Given an image and a normalized pixel map, draw the map on the image."""
    if outline is None:
        outline = (0, 0, 0)
    for pixel in pix_map_normlized:
        pix_coordinate = (
            int(image.shape[0] * pixel[0]),
            int(image.shape[1] * pixel[1])
        )
        cv2.circle(image, pix_coordinate, radius, outline, 1)
    return image
