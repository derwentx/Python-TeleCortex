import random

import cv2
import colorsys
import itertools
import logging
import math
from pprint import pformat


def log_if_correct_level(logging_level, message):
    if logging.getLogger().getEffectiveLevel() == logging_level:
        logging.debug(message)


class PanelDriver(object):

    def __init__(self, pix_map_normlized_smol, pix_map_normlized_big, img_size, max_hue, max_angle):
        self.pix_map_normlized_smol = pix_map_normlized_smol
        self.pix_map_normlized_big = pix_map_normlized_big
        self.img_size = img_size
        self.max_hue = max_hue
        self.max_angle = max_angle

    def direct_rainbows(self, angle=0.):
        pixel_list_smol = self.calc_direct_rainbows(angle, self.pix_map_normlized_smol)
        pixel_list_big = self.calc_direct_rainbows(angle, self.pix_map_normlized_big)

        # log_if_correct_level(logging.DEBUG, "pixel_list returned: %s ... " % (pixel_list_smol[:10]))
        # log_if_correct_level(logging.DEBUG, "pixel_list returned: %s ... " % (pixel_list_big[:10]))
        return pixel_list_smol, pixel_list_big

    def calc_direct_rainbows(self, angle, pix_map_normlized):
        pixel_list = []
        for coordinate in pix_map_normlized:
            magnitude = math.sqrt(
                (0.5 - coordinate[0]) ** 2 +
                (0.5 - coordinate[1]) ** 2
            )
            hue = (magnitude * self.max_hue + angle * self.max_hue / self.max_angle) % self.max_hue
            rgb = tuple(int(c * 255) for c in colorsys.hsv_to_rgb(hue, 1, 1))
            pixel_list.append(rgb)
        # log_if_correct_level(logging.DEBUG, "pixel_list: %s" % pformat(pixel_list))
        return list(itertools.chain(*pixel_list))

    def wtf_jvb_rainbows(self, angle=0., seed=random.random()):
        pixel_list_smol = self.calc_wtf_jvb_rainbows(angle, self.pix_map_normlized_smol, seed)
        pixel_list_big = self.calc_wtf_jvb_rainbows(angle, self.pix_map_normlized_big, seed)
        return pixel_list_smol, pixel_list_big

    def calc_wtf_jvb_rainbows(self, angle, pix_map_normlized, seed):
        pixel_list = []
        speed_factor = 500
        brightness_factor = 0.3
        saturation = 1
        hue = 1
        value = 1

        for coordinate in pix_map_normlized:
            center = (0.5, 0.5)
            magnitude = (
                                (center[0] - coordinate[0]) ** 2 +
                                (center[1] - coordinate[1]) ** 2
                        ) ** (1 / 2)

            sin_baby = angle / speed_factor
            hue = math.sin((magnitude ** 2 + hue ** 2) / 2 * (magnitude + sin_baby / hue) + sin_baby)
            # value = math.sin(-(magnitude**2 + value**2)/2*(sin_baby + value) + magnitude/2) * brightness_factor
            value = 1
            rgb = tuple(int(c * 255) for c in colorsys.hsv_to_rgb(hue, saturation, value))
            pixel_list.append(rgb)
        return list(itertools.chain(*pixel_list))

    def crazy_rainbows(self, angle=0., seed=(random.random() * 50)):
        pixel_list_smol = self.calc_crazy_rainbows(angle, self.pix_map_normlized_smol, seed)
        pixel_list_big = self.calc_crazy_rainbows(angle, self.pix_map_normlized_big, seed)
        return pixel_list_smol, pixel_list_big

    def calc_crazy_rainbows(self, angle, pix_map_normlized, seed):
        pixel_list = []
        speed_factor = 1300
        brightness_factor = 0.3
        saturation = 1
        hue = 10

        for coordinate in pix_map_normlized:
            center = (0.5, 0.5)
            magnitude = (
                (center[0] - coordinate[0]) ** 2 +
                (center[1] - coordinate[1]) ** 2
            )**(1/2)

            sin_baby = (angle+30)/speed_factor
            hue = math.sin((sin_baby**3 + hue**2)/2 + magnitude)
            value = math.sin((sin_baby**2 + hue**4)/2 - seed + magnitude) * brightness_factor
            rgb = tuple(int(c * 255) for c in colorsys.hsv_to_rgb(hue, saturation, value))
            pixel_list.append(rgb)
        return list(itertools.chain(*pixel_list))
