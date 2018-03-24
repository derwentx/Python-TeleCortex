"""Simple Rainbow test script with no mapping required. """

from __future__ import unicode_literals

import itertools
import logging
import os
from datetime import datetime

import serial
from serial.tools import list_ports

import coloredlogs
from context import telecortex
from telecortex.session import (PANEL_LENGTHS, PANELS, TELECORTEX_BAUD,
                                TELECORTEX_VID, find_serial_dev, TelecortexSession)
from telecortex.util import pix_array2text

# STREAM_LOG_LEVEL = logging.DEBUG
# STREAM_LOG_LEVEL = logging.INFO
STREAM_LOG_LEVEL = logging.WARN
# STREAM_LOG_LEVEL = logging.ERROR

LOG_FILE = ".rainbowz.log"
ENABLE_LOG_FILE = True

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.DEBUG)
STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setLevel(STREAM_LOG_LEVEL)
if os.name != 'nt':
    STREAM_HANDLER.setFormatter(coloredlogs.ColoredFormatter())
STREAM_HANDLER.addFilter(coloredlogs.HostNameFilter())
STREAM_HANDLER.addFilter(coloredlogs.ProgramNameFilter())
if ENABLE_LOG_FILE:
    LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(STREAM_HANDLER)

TELECORTEX_DEV = "/dev/tty.usbmodem35"
DO_SINGLE = False


def main():
    """
    Main.

    Enumerate serial ports
    Select board by pid/vid
    Rend some HSV rainbowz
    Respond to microcontroller
    """
    logging.debug("\n\n\nnew session at %s" % datetime.now().isoformat())

    target_device = find_serial_dev(TELECORTEX_VID)
    if target_device is None:
        target_device = TELECORTEX_DEV
    if not target_device:
        raise UserWarning("target device not found")
    else:
        logging.debug("target_device: %s" % target_device)
        logging.debug("baud: %s" % TELECORTEX_BAUD)
    # Connect to serial
    frameno = 0
    with serial.Serial(
        port=target_device, baudrate=TELECORTEX_BAUD, timeout=1
    ) as ser:
        # logging.debug("settings: %s" % pformat(ser.get_settings()))
        sesh = TelecortexSession(ser)
        sesh.reset_board()

        while sesh:

            # H = frameno, S = 255 (0xff), V = 127 (0x7f)
            logging.debug("Drawing frame %s" % frameno)
            for panel in range(PANELS):
                if DO_SINGLE:
                    pixel_str = pix_array2text(
                        frameno, 255, 127
                    )
                    sesh.send_cmd_sync("M2603", {"Q":panel, "V":pixel_str})
                else:
                    panel_length = PANEL_LENGTHS[panel]
                    # logging.debug(
                    #     "panel: %s; panel_length: %s" % (panel, panel_length)
                    # )
                    pixel_list = [
                        [(frameno + pixel) % 256, 255, 127]
                        for pixel in range(panel_length)
                    ]
                    # logging.info("pixel_list: %s" % pformat(pixel_list))
                    pixel_list = list(itertools.chain(*pixel_list))
                    pixel_str = pix_array2text(*pixel_list)
                    sesh.chunk_payload_with_linenum("M2601", {"Q":panel}, pixel_str)
            sesh.send_cmd_with_linenum("M2610")
            frameno = (frameno + 1) % 255


if __name__ == '__main__':
    main()
