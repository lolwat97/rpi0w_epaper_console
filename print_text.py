#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os

import ntplib
from time import ctime

import logging
from waveshare_epd import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

def draw_screen(epd, font, data):
    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
    draw = ImageDraw.Draw(image)
    
    time = data[0]

    draw.text((0, 0), time, font = font, fill = 0)
    epd.display(epd.getbuffer(image))

def get_info():
    time = get_time()
    return [time] 

def get_time():
    response = ntplib.NTPClient().request('europe.pool.ntp.org', version=3)
    return ctime(response.recv_time)

try:
    font8 = ImageFont.truetype('Font.ttc', 8)
    font10 = ImageFont.truetype('Font.ttc', 10)
    font15 = ImageFont.truetype('Font.ttc', 15)
    font24 = ImageFont.truetype('Font.ttc', 24)

    epd = epd2in13_V2.EPD()
    logging.info("init and Clear")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    while(True):
        info = get_info()
        draw_screen(epd, font10, info)
        time.sleep(60)
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()
