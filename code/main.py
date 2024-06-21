#import chardet
import os
import sys
import time
import logging
import spidev as SPI
import pygame
import threading

sys.path.append("..")
from lib import LCD_1inch28
from PIL import Image,ImageDraw,ImageFont

class screenPlayer():
    def __init__(self):
        # Raspberry Pi pin configuration:
        RST = 27
        DC = 25
        BL = 18
        bus = 0
        device = 0
        self.count = 0
        logging.basicConfig(level=logging.DEBUG)
        # display with hardware SPI:
        ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
        # disp = LCD_1inch28.LCD_1inch28(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
        self.disp = LCD_1inch28.LCD_1inch28()
        # Initialize library.
        self.disp.Init()
        # Clear display.
        self.disp.clear()
        # Set the backlight to 100
        self.disp.bl_DutyCycle(50)

        # Create blank image for drawing.
        image1 = Image.new("RGB", (self.disp.width,self.disp.height), "BLACK")
        draw = ImageDraw.Draw(image1)

    def screenPlayer(self, character, mov, state):
        try:
            imageLoc = '../pic/' + character + '/' + mov + state + '.png'
            image = Image.open(imageLoc)
            self.disp.ShowImage(image)
        except IOError as e:
            logging.info(e)

    def module_exit(self):
        self.disp.module_exit()
        logging.info("quit:")


    '''A basic screen player， for a pink ball up and down'''
    def screenController(self):
        try:

            while (self.count < 100):
                sec = 0.2
                for i in range(5):
                    state = 'D' + str(i)
                    self.screenPlayer('Ashin','base',state)
                    time.sleep(sec)
                    if (i >= 2):
                       sec = sec * 5
                    else:
                        sec = sec * 0.2
                sec = 0.2
                for i in range(5):
                    state = 'D' + str(4-i)
                    self.screenPlayer('Ashin', 'base', state)
                    time.sleep(sec)
                    if (i >= 2):
                        sec = sec * 5
                    else:
                        sec = sec * 0.2
                self.count += 1
        except IOError as e:
            logging.info(e)
        except KeyboardInterrupt:
            self.disp.module_exit()
            logging.info("quit:")
            exit()

class musicPlayer():
    def __init__(self):
        self.isStop = False
        pygame.mixer.init()

    def musicPlayer(self, music):
        pygame.mixer.music.load(music)
        pygame.mixer.music.play()

    def musicStop(self):
        pygame.mixer.music.stop()


if __name__ == "__main__":
    s = screenPlayer()
    s.screenController()
    s.module_exit()

    m = musicPlayer()
    m.musicPlayer('../music/五月天 - 你说那 C 和弦就是....mp3')
    time.sleep(20)
    m.musicStop()

    screenController_thread = threading.Thread(target=s.screenController, args=())
    musicPlayer_thread = threading.Thread(target=m.musicPlayer, args=('../music/五月天 - 你说那 C 和弦就是....mp3'))
    screenController_thread.start()
    musicPlayer_thread.start()
    time.sleep(20)
    s.count = 100
    m.isStop = True
    m.musicStop()
    logging.info(screenController_thread.isAlive())
    while(s.disp.digital_read())