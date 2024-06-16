#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
import os
import sys 
import time
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_1inch28
from PIL import Image,ImageDraw,ImageFont

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level=logging.DEBUG)
try:
    # display with hardware SPI:
    ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
    #disp = LCD_1inch28.LCD_1inch28(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
    disp = LCD_1inch28.LCD_1inch28()
    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()
    #Set the backlight to 100
    disp.bl_DutyCycle(50)

    # Create blank image for drawing.
    image1 = Image.new("RGB", (disp.width, disp.height), "BLACK")
    draw = ImageDraw.Draw(image1)

    #logging.info("draw point")
    #draw.rectangle((Xstart,Ystart,Xend,Yend), fill = "color")
    logging.info("draw circle")
    draw.arc((1,1,239,239),0, 360, fill =(0,0,255))
    draw.arc((2,2,238,238),0, 360, fill =(0,0,255))
    draw.arc((3,3,237,237),0, 360, fill =(0,0,255))
    
    logging.info("draw dial line")
    draw.line([(120, 1),(120, 12)], fill = (128,255,128),width = 4)
    draw.line([(120, 227),(120, 239)], fill = (128,255,128),width = 4)
    draw.line([(1,120),(12,120)], fill = (128,255,128),width = 4)
    draw.line([(227,120),(239,120)], fill = (128,255,128),width = 4)

    logging.info("draw text")
    Font1 = ImageFont.truetype("../Font/Font01.ttf",25)
    Font2 = ImageFont.truetype("../Font/Font01.ttf",35)
    Font3 = ImageFont.truetype("../Font/Font02.ttf",32)

    draw.text((40, 50), 'WaveShare', fill = (128,255,128),font=Font2)
    text= u"微雪电子"
    draw.text((74, 150),text, fill = "WHITE",font=Font3)
    
    logging.info("draw pointer line")
    draw.line([(120, 120),(70, 70)], fill = "YELLOW",width = 3)
    draw.line([(120, 120),(176, 64)], fill = "BLUE",width = 3)
    draw.line([(120, 120),(120 ,210)], fill = "RED",width = 3)   
 
    im_r=image1.rotate(180)
    disp.ShowImage(im_r)
    time.sleep(3)
    count = 0
    while(count < 100):
        logging.info("show image1")
        image = Image.open('../pic/xinbase.png')
        im_r = image.rotate(180)
        disp.ShowImage(im_r)
        time.sleep(3)
        logging.info("show image1")
        image = Image.open('../pic/xinbaseD0.png')
        im_r = image.rotate(180)
        disp.ShowImage(im_r)
        time.sleep(3)
        logging.info("show image1")
        image = Image.open('../pic/xinbaseD1.png')
        im_r = image.rotate(180)
        disp.ShowImage(im_r)
        time.sleep(3)
        logging.info("show image1")
        image = Image.open('../pic/xinbaseD2.png')
        im_r = image.rotate(180)
        disp.ShowImage(im_r)
        time.sleep(3)
        logging.info("show image1")
        image = Image.open('../pic/xinbaseD3.png')
        im_r = image.rotate(180)
        disp.ShowImage(im_r)
        time.sleep(3)
        count += 1

    disp.module_exit()
    logging.info("quit:")
except IOError as e:
    logging.info(e)    
except KeyboardInterrupt:
    disp.module_exit()
    logging.info("quit:")
    exit()