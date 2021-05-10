#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import requests

import get_twitter_followers

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
        self.webdriver = get_twitter_followers.open_driver()
        self.data = []

    def init_screen(self):
        logging.info("init and Clear")
        self.epd.init(self.epd.FULL_UPDATE)
        self.epd.Clear(0xFF)


    def draw_screen(self):
        image = Image.new('1', (self.epd.height, self.epd.width), 255)
        draw = ImageDraw.Draw(image)
        
        time = self.data[0]
        twitter_followers = 'Follower count for @lolwatve: ' + self.data[1]

        draw.text((0, 0), time, font = self.font10, fill = 0)
        draw.text((0, 15), twitter_followers, font = self.font10, fill=0)
        self.epd.display(self.epd.getbuffer(image))

    def get_info(self):
        time = self.get_time()
        twitter_followers = get_twitter_followers.get_follower_count(self.webdriver)
        self.data = [time, twitter_followers]

    def get_time(self):
        response = ntplib.NTPClient().request('europe.pool.ntp.org', version=3)
        return ctime(response.recv_time)

    def get_request(self, url):
        response = requests.get(url).text
        return response

    def run(self):
        try:
            self.init_screen()
            while(True):
                try:
                    self.draw_screen()
                    time.sleep(60)
                except Exception as e:
                    logging.error(str(e))
                    time.sleep(10)
    
        except IOError as e:
            logging.info(e)
            
        except KeyboardInterrupt:    
            logging.info("ctrl + c:")
            epd2in13_V2.epdconfig.module_exit()
            get_twitter_followers.close_driver(self.webdriver)
            exit()

console = Console()
console.run()