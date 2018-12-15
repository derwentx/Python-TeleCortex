"""Module for mapping panel pixels to animation pixels."""

import sys, os
import numpy as np
from collections import OrderedDict
from .interpolation import denormalize_coordinate
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
PIXEL_MAP_DOME_SMOL = PIXEL_MAP_SMOL

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
PIXEL_MAP_DOME_BIG = PIXEL_MAP_BIG

PIXEL_MAP_OUTER = np.array([
    [431, 1515], [449, 1511], [454, 1494], [464, 1508], [473, 1523],
    [489, 1518], [480, 1504], [471, 1491], [476, 1475], [486, 1488],
    [495, 1500], [504, 1513], [514, 1526], [538, 1535], [528, 1522],
    [519, 1509], [510, 1496], [500, 1483], [490, 1470], [481, 1457],
    [489, 1441], [498, 1454], [508, 1468], [517, 1481], [526, 1494],
    [536, 1507], [545, 1520], [555, 1534], [564, 1547], [579, 1543],
    [569, 1530], [560, 1516], [550, 1503], [540, 1490], [530, 1477],
    [520, 1464], [511, 1450], [501, 1437], [509, 1424], [519, 1437],
    [528, 1450], [538, 1463], [547, 1476], [557, 1488], [567, 1501],
    [576, 1514], [586, 1527], [595, 1540], [605, 1553], [629, 1561],
    [620, 1548], [610, 1535], [601, 1522], [591, 1509], [582, 1496],
    [572, 1484], [563, 1471], [554, 1458], [544, 1445], [535, 1432],
    [525, 1419], [516, 1406], [533, 1402], [542, 1415], [552, 1428],
    [561, 1441], [570, 1454], [580, 1467], [589, 1480], [598, 1493],
    [608, 1506], [617, 1519], [626, 1532], [636, 1545], [645, 1558],
    [667, 1567], [658, 1554], [648, 1541], [639, 1528], [630, 1516],
    [620, 1503], [611, 1490], [602, 1477], [592, 1464], [583, 1451],
    [573, 1438], [564, 1426], [555, 1413], [545, 1400], [536, 1387],
    [543, 1370], [552, 1383], [562, 1396], [571, 1409], [580, 1422],
    [590, 1435], [599, 1448], [609, 1461], [618, 1474], [627, 1486],
    [637, 1499], [646, 1512], [656, 1525], [665, 1538], [674, 1551],
    [684, 1564], [693, 1577], [708, 1572], [699, 1559], [689, 1546],
    [680, 1533], [671, 1520], [661, 1507], [652, 1494], [643, 1481],
    [634, 1468], [624, 1456], [615, 1443], [606, 1430], [596, 1417],
    [587, 1404], [578, 1391], [568, 1378], [559, 1365], [565, 1351],
    [574, 1364], [584, 1377], [593, 1390], [603, 1403], [612, 1415],
    [621, 1428], [631, 1441], [640, 1454], [650, 1467], [659, 1480],
    [668, 1493], [678, 1506], [687, 1519], [696, 1531], [706, 1544],
    [715, 1557], [725, 1570], [734, 1583], [758, 1591], [749, 1578],
    [739, 1565], [730, 1553], [721, 1540], [711, 1527], [702, 1514],
    [693, 1501], [683, 1489], [674, 1476], [664, 1463], [655, 1450],
    [646, 1437], [636, 1425], [627, 1412], [618, 1399], [608, 1386],
    [599, 1373], [590, 1361], [580, 1348], [571, 1335], [587, 1330],
    [596, 1343], [606, 1356], [615, 1369], [624, 1382], [634, 1395],
    [643, 1408], [652, 1421], [662, 1434], [671, 1447], [680, 1460],
    [690, 1473], [699, 1486], [709, 1499], [718, 1512], [727, 1525],
    [737, 1538], [746, 1551], [755, 1564], [765, 1577], [774, 1590],
    [801, 1598], [792, 1585], [782, 1572], [772, 1559], [763, 1546],
    [754, 1533], [744, 1521], [734, 1508], [725, 1495], [716, 1482],
    [706, 1469], [696, 1456], [687, 1443], [678, 1430], [668, 1417],
    [658, 1404], [649, 1391], [640, 1379], [630, 1366], [620, 1353],
    [611, 1340], [602, 1327], [592, 1314], [600, 1298], [609, 1311],
    [619, 1324], [628, 1337], [637, 1350], [646, 1363], [656, 1376],
    [665, 1389], [674, 1402], [684, 1415], [693, 1428], [702, 1441],
    [712, 1454], [721, 1466], [730, 1479], [739, 1492], [749, 1505],
    [758, 1518], [767, 1531], [777, 1544], [786, 1557], [795, 1570],
    [804, 1583], [814, 1596], [823, 1609], [849, 1617], [840, 1604],
    [830, 1591], [820, 1578], [811, 1565], [802, 1552], [792, 1539],
    [782, 1526], [773, 1513], [764, 1500], [754, 1487], [744, 1474],
    [735, 1461], [726, 1448], [716, 1436], [706, 1423], [697, 1410],
    [688, 1397], [678, 1384], [668, 1371], [659, 1358], [650, 1345],
    [640, 1332], [630, 1319], [621, 1306], [612, 1293], [602, 1280]
])
PIXEL_MAP_DOME_OUTER = PIXEL_MAP_OUTER

PIXEL_MAP_OUTER_FLIP = np.array([
    [1327, 1519], [1312, 1513], [1287, 1524], [1298, 1509], [1308, 1494],
    [1292, 1492], [1282, 1506], [1273, 1521], [1249, 1529], [1258, 1516],
    [1267, 1502], [1276, 1489], [1285, 1476], [1277, 1461], [1268, 1474],
    [1259, 1487], [1250, 1500], [1240, 1513], [1231, 1526], [1222, 1539],
    [1199, 1547], [1208, 1534], [1218, 1521], [1227, 1508], [1236, 1495],
    [1246, 1482], [1255, 1469], [1265, 1456], [1274, 1443], [1257, 1438],
    [1248, 1451], [1238, 1464], [1229, 1477], [1220, 1490], [1211, 1503],
    [1202, 1516], [1192, 1529], [1183, 1542], [1158, 1551], [1167, 1538],
    [1176, 1525], [1186, 1512], [1195, 1499], [1204, 1486], [1213, 1474],
    [1222, 1461], [1232, 1448], [1241, 1435], [1250, 1422], [1244, 1406],
    [1235, 1419], [1225, 1432], [1216, 1445], [1207, 1458], [1197, 1471],
    [1188, 1484], [1179, 1496], [1169, 1509], [1160, 1522], [1151, 1535],
    [1141, 1548], [1132, 1561], [1118, 1558], [1127, 1545], [1137, 1532],
    [1146, 1519], [1156, 1506], [1165, 1493], [1174, 1480], [1184, 1467],
    [1193, 1454], [1203, 1441], [1212, 1428], [1222, 1415], [1231, 1402],
    [1223, 1382], [1214, 1395], [1204, 1409], [1195, 1422], [1186, 1435],
    [1176, 1449], [1167, 1462], [1158, 1476], [1148, 1489], [1139, 1502],
    [1129, 1516], [1120, 1529], [1111, 1542], [1101, 1556], [1092, 1569],
    [1067, 1577], [1076, 1564], [1086, 1551], [1095, 1538], [1104, 1525],
    [1114, 1512], [1123, 1499], [1133, 1486], [1142, 1474], [1151, 1461],
    [1161, 1448], [1170, 1435], [1180, 1422], [1189, 1409], [1198, 1396],
    [1208, 1383], [1217, 1370], [1201, 1367], [1192, 1380], [1182, 1393],
    [1173, 1406], [1164, 1419], [1154, 1432], [1145, 1445], [1135, 1458],
    [1126, 1471], [1117, 1484], [1107, 1497], [1098, 1510], [1088, 1523],
    [1079, 1536], [1070, 1549], [1060, 1562], [1051, 1575], [1027, 1583],
    [1036, 1570], [1046, 1557], [1056, 1544], [1065, 1531], [1074, 1519],
    [1084, 1506], [1094, 1493], [1103, 1480], [1112, 1467], [1122, 1454],
    [1132, 1441], [1141, 1428], [1150, 1415], [1160, 1403], [1170, 1390],
    [1179, 1377], [1188, 1364], [1198, 1351], [1190, 1333], [1181, 1346],
    [1171, 1359], [1162, 1372], [1153, 1385], [1143, 1398], [1134, 1411],
    [1125, 1424], [1115, 1437], [1106, 1450], [1096, 1463], [1087, 1476],
    [1078, 1489], [1068, 1502], [1059, 1515], [1050, 1528], [1040, 1541],
    [1031, 1554], [1022, 1567], [1012, 1580], [1003, 1593], [987, 1588],
    [996, 1575], [1006, 1562], [1015, 1549], [1025, 1537], [1034, 1524],
    [1043, 1511], [1053, 1498], [1062, 1485], [1072, 1472], [1081, 1460],
    [1090, 1447], [1100, 1434], [1109, 1421], [1119, 1408], [1128, 1395],
    [1137, 1382], [1147, 1370], [1156, 1357], [1166, 1344], [1175, 1331],
    [1169, 1312], [1160, 1325], [1150, 1338], [1141, 1351], [1132, 1364],
    [1122, 1377], [1113, 1390], [1103, 1403], [1094, 1416], [1085, 1429],
    [1075, 1442], [1066, 1456], [1057, 1469], [1047, 1482], [1038, 1495],
    [1029, 1508], [1019, 1521], [1010, 1534], [1000, 1547], [991, 1560],
    [982, 1573], [972, 1586], [963, 1599], [938, 1605], [947, 1592],
    [957, 1579], [966, 1566], [976, 1554], [985, 1541], [994, 1528],
    [1004, 1515], [1013, 1502], [1022, 1489], [1032, 1476], [1041, 1463],
    [1050, 1450], [1060, 1438], [1069, 1425], [1079, 1412], [1088, 1399],
    [1097, 1386], [1107, 1373], [1116, 1360], [1126, 1348], [1135, 1335],
    [1144, 1322], [1154, 1309], [1163, 1296], [1156, 1280], [1147, 1293],
    [1137, 1306], [1128, 1319], [1118, 1332], [1109, 1345], [1100, 1358],
    [1090, 1371], [1081, 1384], [1072, 1397], [1062, 1410], [1053, 1423],
    [1043, 1436], [1034, 1449], [1025, 1462], [1015, 1475], [1006, 1488],
    [996, 1501], [987, 1514], [978, 1527], [968, 1540], [959, 1553],
    [950, 1566], [940, 1579], [931, 1592], [921, 1605],
    [912, 1618]
])
PIXEL_MAP_DOME_OUTER_FLIP = PIXEL_MAP_OUTER_FLIP

PIXEL_MAP_GOGGLE = np.array(
    [
        [-1, -1]
    ] * 16 + [
        [1, 1]
    ] * 16
)

def normalize_pix_map(pix_map):
    """Return a normalized copy of `pixel map` all x, y between 0, 1."""
    assert isinstance(pix_map, np.ndarray), \
        "pix_map should be a numpy ndarray, not %s" % type(pix_map)
    assert pix_map.shape[1] == 2, \
        "pix map should be an array of 2d coordinates, not shape: %s" % (pix_map.shape, )
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

MAPS_DOME_SIMPLIFIED = OrderedDict([
    ('smol', normalize_pix_map(PIXEL_MAP_DOME_SMOL)),
    ('big', normalize_pix_map(PIXEL_MAP_DOME_BIG)),
])

MAPS_DOME = OrderedDict([
    ('smol', normalize_pix_map(PIXEL_MAP_DOME_SMOL)),
    ('big', normalize_pix_map(PIXEL_MAP_DOME_BIG)),
    ('outer', normalize_pix_map(PIXEL_MAP_DOME_OUTER)),
    ('outer_flip', normalize_pix_map(PIXEL_MAP_DOME_OUTER_FLIP))
])

MAPS_GOGGLE = OrderedDict([
    ('goggle', normalize_pix_map(PIXEL_MAP_GOGGLE))
])

def mat_rotation_2d(angle):
    """
    Generate a rotation matrix from the angle in degrees.
    """
    theta = np.radians(angle)
    val_cos, val_sin = np.cos(theta), np.sin(theta)
    return np.matrix([[val_cos, -val_sin], [val_sin, val_cos]])

def mat_scale_2d(scalar):
    """
    Generate a scale matrix from the scalar.
    """
    return np.matrix([[scalar, 0], [0, scalar]])

def mat_scale_2d_y(scalar):
    """
    Generate a scale matrix in the y direction from the scalar
    """
    return np.matrix([[1, 0], [0, scalar]])

def vector_transform(vector, matrix):
    # TODO: fix this math
    return np.asarray(matrix * np.asmatrix(vector).transpose()).transpose()[0]

def rotate_vector(vector, angle):
    mat = mat_rotation_2d(angle)
    return vector_transform(vector, mat)

def transform_mapping(mapping, mat):
    return [
        vector_transform(coordinate, mat)
        for coordinate in mapping
    ]

def scale_mapping(mapping, scale):
    if type(scale) == int:
        return [
            scale * coordinate \
            for coordinate in mapping
        ]
    elif type(scale) == np.matrix:
        return transform_mapping(mapping, scale)

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

GLOBAL_SCALE = 0.6
PANEL_0_SKEW = mat_scale_2d_y(0.8) * mat_rotation_2d(-60) * mat_scale_2d(0.5 * GLOBAL_SCALE)
PANEL_0_OFFSET = (-0.042 * GLOBAL_SCALE, 0.495 * GLOBAL_SCALE)
PANEL_1_SKEW = mat_scale_2d_y(0.95) * mat_scale_2d(0.5 * GLOBAL_SCALE)
PANEL_1_OFFSET = (0, 0.26 * GLOBAL_SCALE)
PANEL_2_SKEW = np.matrix([[1.1 * GLOBAL_SCALE, 0], [0, 1.1 * GLOBAL_SCALE]])
PANEL_2_OFFSET = (0.09 * GLOBAL_SCALE, 0.11 * GLOBAL_SCALE)
PANEL_3_SKEW = np.matrix([[0.4 * GLOBAL_SCALE, 0], [0, 0.4 * GLOBAL_SCALE]])
PANEL_3_OFFSET = (0.25 * GLOBAL_SCALE, 0.65 * GLOBAL_SCALE)
CTRL_1_ROT = (1 * 360 / 5)
CTRL_2_ROT = (2 * 360 / 5)
CTRL_3_ROT = (3 * 360 / 5)
CTRL_4_ROT = (4 * 360 / 5)
CTRL_5_ROT = (0 * 360 / 5)


GENERATOR_DOME_OVERHEAD = OrderedDict([
    (0, [
        (0, 'big', PANEL_0_SKEW, CTRL_1_ROT, rotate_vector(PANEL_0_OFFSET, CTRL_1_ROT)),
        (1, 'smol', PANEL_1_SKEW, CTRL_1_ROT, rotate_vector(PANEL_1_OFFSET, CTRL_1_ROT)),
        (2, 'outer', PANEL_2_SKEW, CTRL_1_ROT, rotate_vector(PANEL_2_OFFSET, CTRL_1_ROT)),
        # (3, 'outer_flip', PANEL_3_SKEW, (CTRL_1_ROT + CTRL_1_ROT), rotate_vector(PANEL_3_OFFSET, (CTRL_1_ROT + CTRL_1_ROT))),
    ]),
    (1, [
        (0, 'big', PANEL_0_SKEW, CTRL_2_ROT, rotate_vector(PANEL_0_OFFSET, CTRL_2_ROT)),
        (1, 'smol', PANEL_1_SKEW, CTRL_2_ROT, rotate_vector(PANEL_1_OFFSET, CTRL_2_ROT)),
        # # (2, 'outer', PANEL_2_SKEW, CTRL_2_ROT, rotate_vector(PANEL_2_OFFSET, CTRL_2_ROT)),
        # # (3, 'outer_flip', PANEL_3_SKEW, (CTRL_2_ROT + CTRL_1_ROT), rotate_vector(PANEL_3_OFFSET, (CTRL_2_ROT + CTRL_1_ROT))),
    ]),
    (2, [
        (0, 'big', PANEL_0_SKEW, CTRL_3_ROT, rotate_vector(PANEL_0_OFFSET, CTRL_3_ROT)),
        (1, 'smol', PANEL_1_SKEW, CTRL_3_ROT, rotate_vector(PANEL_1_OFFSET, CTRL_3_ROT)),
        # # (2, 'outer', PANEL_2_SKEW, CTRL_3_ROT, rotate_vector(PANEL_2_OFFSET, CTRL_3_ROT)),
        (3, 'outer_flip', PANEL_3_SKEW, (CTRL_3_ROT + CTRL_1_ROT), rotate_vector(PANEL_3_OFFSET, (CTRL_3_ROT + CTRL_1_ROT))),
    ]),
    (3, [
        (0, 'big', PANEL_0_SKEW, CTRL_4_ROT, rotate_vector(PANEL_0_OFFSET, CTRL_4_ROT)),
        (1, 'smol', PANEL_1_SKEW, CTRL_4_ROT, rotate_vector(PANEL_1_OFFSET, CTRL_4_ROT)),
        (2, 'outer', PANEL_2_SKEW, CTRL_4_ROT, rotate_vector(PANEL_2_OFFSET, CTRL_4_ROT)),
        (3, 'outer_flip', PANEL_3_SKEW, (CTRL_4_ROT + CTRL_1_ROT), rotate_vector(PANEL_3_OFFSET, (CTRL_4_ROT + CTRL_1_ROT))),
    ]),
    (4, [
        (0, 'big', PANEL_0_SKEW, CTRL_5_ROT, rotate_vector(PANEL_0_OFFSET, CTRL_5_ROT)),
        (1, 'smol', PANEL_1_SKEW, CTRL_5_ROT, rotate_vector(PANEL_1_OFFSET, CTRL_5_ROT)),
        (2, 'outer', PANEL_2_SKEW, CTRL_5_ROT, rotate_vector(PANEL_2_OFFSET, CTRL_5_ROT)),
        (3, 'outer_flip', PANEL_3_SKEW, (CTRL_5_ROT + CTRL_1_ROT), rotate_vector(PANEL_3_OFFSET, (CTRL_5_ROT + CTRL_1_ROT))),
    ])
])

GENERATOR_DOME_DJ = OrderedDict([
    # To do
])


TRIF_GLOBAL_SCALE = 0.45
TRIF_PANEL_0_SKEW = mat_scale_2d(TRIF_GLOBAL_SCALE) * mat_rotation_2d(0)
TRIF_PANEL_0_OFFSET = (0.2 * TRIF_GLOBAL_SCALE, 0)
TRIF_PANEL_1_SKEW = mat_scale_2d(TRIF_GLOBAL_SCALE)
TRIF_PANEL_1_OFFSET = (-0.6 * TRIF_GLOBAL_SCALE, 0)

GENERATOR_TRIFORCE = OrderedDict([
    (0, [
        (0, 'big', TRIF_PANEL_0_SKEW, 90, TRIF_PANEL_0_OFFSET),
        (1, 'big', TRIF_PANEL_1_SKEW, -90, rotate_vector(TRIF_PANEL_1_OFFSET, 0)),
        (2, 'big', TRIF_PANEL_1_SKEW, -90, rotate_vector(TRIF_PANEL_1_OFFSET, 120)),
        (3, 'big', TRIF_PANEL_1_SKEW, -90, rotate_vector(TRIF_PANEL_1_OFFSET, 240))
    ])
])

DOME_TRIF_GLOBAL_SCALE = 0.45
DOME_TRIF_PANEL_0_SKEW = mat_scale_2d(DOME_TRIF_GLOBAL_SCALE) * mat_rotation_2d(0)
DOME_TRIF_PANEL_0_OFFSET = (0.1 * DOME_TRIF_GLOBAL_SCALE, 0)
DOME_TRIF_PANEL_1_SKEW = mat_scale_2d(DOME_TRIF_GLOBAL_SCALE)
DOME_TRIF_PANEL_1_OFFSET = (-0.6 * DOME_TRIF_GLOBAL_SCALE, 0)

GENERATOR_DOME_TRIFORCE = OrderedDict([
    (0, [
        (0, 'big', DOME_TRIF_PANEL_0_SKEW, 90, DOME_TRIF_PANEL_0_OFFSET),
        (1, 'smol', DOME_TRIF_PANEL_1_SKEW, -90, rotate_vector(DOME_TRIF_PANEL_1_OFFSET, 0)),
        (2, 'smol', DOME_TRIF_PANEL_1_SKEW, -90 + 120, rotate_vector(DOME_TRIF_PANEL_1_OFFSET, 120)),
        (3, 'smol', DOME_TRIF_PANEL_1_SKEW, -90 + 240, rotate_vector(DOME_TRIF_PANEL_1_OFFSET, 240))
    ])
])

PANELS_DOME_SIMPLIFIED = OrderedDict([
    (0, [
        (0, 'big'),
        (1, 'smol'),
        (2, 'smol'),
        (3, 'smol')
    ]),
    (1, [
        (0, 'big'),
        (1, 'smol'),
        (2, 'smol'),
        (3, 'smol')
    ]),
    (2, [
        (0, 'big'),
        (1, 'smol'),
        (2, 'smol'),
        (3, 'smol')
    ]),
    (3, [
        (0, 'big'),
        (1, 'smol'),
        (2, 'smol'),
        (3, 'smol')
    ]),
    (4, [
        (0, 'big'),
        (1, 'smol'),
        (2, 'smol'),
        (3, 'smol')
    ])
])

PANELS_GOGGLE = OrderedDict([
    (0, [
        (0, 'goggle')
    ])
])

def transform_panel_map(panel_map, size, scale, angle, offset):
    panel_map = transpose_mapping(panel_map, (-0.5, -0.5))
    panel_map = scale_mapping(panel_map, scale)
    panel_map = rotate_mapping(panel_map, angle)
    panel_map = transpose_mapping(panel_map, (+0.5, +0.5))
    panel_map = transpose_mapping(panel_map, offset)
    return panel_map


def generate_panel_maps(generator):
    maps = OrderedDict()
    panels = OrderedDict()
    for server_id, server_panel_info in generator.items():
        panels[server_id] = []
        maps[server_id] = []
        for panel_number, size, scale, angle, offset in server_panel_info:
            map_name = "%s-%d-%d" % (size, server_id, panel_number)
            if size not in MAPS_DOME:
                raise UserWarning('Panel size %s not in known mappings: %s' %(
                    size, MAPS_DOME.keys()
                ))
            panel_map = MAPS_DOME[size]
            panel_map = transform_panel_map(panel_map, size, scale, angle, offset)

            panels[server_id].append((panel_number, map_name))
            maps[map_name] = panel_map
    return maps, panels


MAPS_DOME_OVERHEAD, PANELS_DOME_OVERHEAD = generate_panel_maps(GENERATOR_DOME_OVERHEAD)
MAPS_DOME_DJ, PANELS_DOME_DJ = generate_panel_maps(GENERATOR_DOME_DJ)
MAPS_DOME_TRIFORCE, PANELS_DOME_TRIFORCE = generate_panel_maps(GENERATOR_DOME_TRIFORCE)
MAPS_TRIFORCE, PANELS_TRIFORCE = generate_panel_maps(GENERATOR_TRIFORCE)

PANELS_PER_CONTROLLER = 4

def draw_map(image, pix_map_normlized, radius=1, outline=None):
    """Given an image and a normalized pixel map, draw the map on the image."""
    if outline is None:
        outline = (0, 0, 0)
    for pixel in pix_map_normlized:
        pix_coordinate = denormalize_coordinate(image.shape, pixel)
        pix_coordinate = (
            int(pix_coordinate[1]),
            int(pix_coordinate[0])
        )
        cv2.circle(image, pix_coordinate, radius, outline, 1)
    return image
