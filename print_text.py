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

class Console():
    def __init__(self):
            self.font8 = ImageFont.truetype('Font.ttc', 8)
            self.font10 = ImageFont.truetype('Font.ttc', 10)
            self.font15 = ImageFont.truetype('Font.ttc', 15)
            self.font24 = ImageFont.truetype('Font.ttc', 24)

            self.epd = epd2in13_V2.EPD()

    def init_screen(self):
        logging.info("init and Clear")
        self.epd.init(self.epd.FULL_UPDATE)
        self.epd.Clear(0xFF)


    def draw_screen(self, epd, font, data):
        image = Image.new('1', (self.epd.height, self.epd.width), 255)  # 255: clear the frame    
        draw = ImageDraw.Draw(image)
        
        time = data[0]

        draw.text((0, 0), time, font = font, fill = 0)
        self.epd.display(self.epd.getbuffer(image))

    def get_info(self):
        time = self.get_time()
        return [time] 

    def get_time(self):
        response = ntplib.NTPClient().request('europe.pool.ntp.org', version=3)
        return ctime(response.recv_time)

    def run(self):
        try:
            self.init_screen()
            while(True):
                info = self.get_info()
                self.draw_screen(self.epd, self.font10, info)
                time.sleep(60)
    
        except IOError as e:
            logging.info(e)
            
        except KeyboardInterrupt:    
            logging.info("ctrl + c:")
            epd2in13_V2.epdconfig.module_exit()
            exit()

console = Console()
console.run()