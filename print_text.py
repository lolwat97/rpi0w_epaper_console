#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os

import logging
from waveshare_epd import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

def draw_screen(epd, font):
    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
    draw = ImageDraw.Draw(image)
    
    draw.text((120, 60), 'penis music', font = font, fill = 0)
    epd.display(epd.getbuffer(image))

def get_info():
    pass


try:
    font15 = ImageFont.truetype('Font.ttc', 15)
    font24 = ImageFont.truetype('Font.ttc', 24)

    epd = epd2in13_V2.EPD()
    logging.info("init and Clear")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    while(True):
        get_info()
        draw_screen(epd, font15)
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()
