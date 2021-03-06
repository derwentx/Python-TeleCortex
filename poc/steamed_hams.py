#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
from collections import OrderedDict
from datetime import datetime
from pprint import pformat
from time import time as time_now

import coloredlogs
import cv2
import numpy as np
# noinspection PyUnresolvedReferences
from context import telecortex
from mss import mss
from telecortex.config import TeleCortexManagerConfig
from telecortex.graphics import (cv2_draw_map, cv2_setup_main_window,
                                 cv2_show_preview)
from telecortex.interpolation import interpolate_pixel_map
from telecortex.manage import TelecortexSessionManager
from telecortex.util import pix_array2text

TARGET_FRAMERATE = 20
MAIN_WINDOW = 'image_window'
# INTERPOLATION_TYPE = 'bilinear'
INTERPOLATION_TYPE = 'nearest'
DOT_RADIUS = 3

# viewport definition
MON = {'top': 200, 'left': 200, 'width': 400, 'height': 400}

def main():
    """
    Main.

    Enumerate serial ports
    Select board by pid/vid
    Rend some perpendicular rainbowz
    Respond to microcontroller
    """

    conf = TeleCortexManagerConfig(
        name="hams",
        description="take the output of the screen and draw on several telecortex controllers",
        default_config='dome_overhead'
    )

    conf.parser.add_argument('--enable-preview', default=False,
                             action='store_true')

    conf.parse_args()

    logging.debug("\n\n\nnew session at %s" % datetime.now().isoformat())

    sct = mss()

    img = np.array(sct.grab(MON))

    if conf.args.enable_preview:
        cv2_setup_main_window(img)

    manager = conf.setup_manager()

    while any([manager.sessions.get(server_id) for server_id in conf.panels]):

        img = np.array(sct.grab(MON))

        cv2.imshow(MAIN_WINDOW, np.array(img))

        for server_id, server_panel_info in conf.panels.items():
            if not manager.sessions.get(server_id):
                continue
            for panel_number, map_name in server_panel_info:
                panel_map = conf.maps[map_name]

                pixel_list = interpolate_pixel_map(
                    img, panel_map, INTERPOLATION_TYPE
                )
                pixel_str = pix_array2text(*pixel_list)

                manager.sessions[server_id].chunk_payload_with_linenum(
                    "M2600", {"Q": panel_number}, pixel_str
                )
            manager.sessions[server_id].send_cmd_with_linenum('M2610')


        if conf.args.enable_preview:
            if cv2_show_preview(img, conf.maps):
                break


if __name__ == '__main__':
    main()
