#import chardet
import os
import sys
import time
import logging
import spidev as SPI
import pygame
import threading
import RPi.GPIO as GPIO


sys.path.append("..")
from lib import LCD_1inch28
from PIL import Image,ImageDraw,ImageFont

character = 2
count = 0
musicIsStop = False
# 切换角色 右移一位
def changeRightCharacter():
    global character
    character = (character + 1) % 5

# 切换角色 左移一位
def changeLeftCharacter():
    global character
    character = (character + 5 - 1) % 5

# 屏幕类
class screenPlayer():
    # 初始化引脚设置
    def __init__(self):
        # Raspberry Pi pin configuration:
        RST = 27
        DC = 25
        BL = 18
        bus = 0
        device = 0
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
        # 按照舞台顺序
        self.ball = ['Monster','Masa','Ashin','Stone','Ming']

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
            global count
            count = 0
            while (count >= 0):
                sec = 0.2
                for i in range(5):
                    state = 'D' + str(i)
                    self.screenPlayer(self.ball[character],'base',state)
                    time.sleep(sec)
                    if (i >= 2):
                       sec = sec * 5
                    else:
                        sec = sec * 0.2
                sec = 0.2
                for i in range(5):
                    state = 'D' + str(4-i)
                    self.screenPlayer(self.ball[character], 'base', state)
                    time.sleep(sec)
                    if (i >= 2):
                        sec = sec * 5
                    else:
                        sec = sec * 0.2
                count += 1
        except IOError as e:
            logging.info(e)
        except KeyboardInterrupt:
            self.disp.module_exit()
            logging.info("quit:")
            exit()

class musicPlayer():
    def __init__(self):
        global musicIsStop
        musicIsStop = False
        pygame.mixer.init()

    def musicPlayer(self, music):
        pygame.mixer.music.load(music)
        pygame.mixer.music.play()

    def musicStop(self):
        while True:
            if musicIsStop == False:
                pygame.mixer.music.stop()
                break;

class controller():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.button_up = 21
        self.button_down = 20
        self.button_left = 16
        self.button_right = 19
        self.button_mid = 13
        self.button_set = 6
        self.button_rst = 5
        GPIO.setup(self.button_mid, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.button_down, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.button_up, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.button_left, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.button_right, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.button_set, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.button_rst, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.button_up, GPIO.FALLING, callback=self.keyCallback, bouncetime=200)
        GPIO.add_event_detect(self.button_down, GPIO.FALLING, callback=self.keyCallback, bouncetime=200)
        GPIO.add_event_detect(self.button_left, GPIO.FALLING, callback=self.keyCallback, bouncetime=200)
        GPIO.add_event_detect(self.button_right, GPIO.FALLING, callback=self.keyCallback, bouncetime=200)
        GPIO.add_event_detect(self.button_mid, GPIO.FALLING, callback=self.keyCallback, bouncetime=200)
        GPIO.add_event_detect(self.button_set, GPIO.FALLING, callback=self.keyCallback, bouncetime=200)
        GPIO.add_event_detect(self.button_rst, GPIO.FALLING, callback=self.keyCallback, bouncetime=200)

    def controllerThread(self):
        while True:
           continue

    def keyCallback(self,key):
        if key == self.button_up:
            print('up')
        elif key == self.button_down:
            print('down')
        elif key == self.button_left:
            changeLeftCharacter()
            print('left')
        elif key == self.button_right:
            changeRightCharacter()
            print('right')
        elif key == self.button_mid:
            print('mid')
        elif key == self.button_set:
            global count
            count = -100
            global musicIsStop
            musicIsStop = False
            print('set')
        elif key == self.button_rst:
            print('rst')
        
        time.sleep(1)




if __name__ == "__main__":
    
    c = controller()
    s = screenPlayer()
    '''s.screenController()'''
    '''s.module_exit()'''

    m = musicPlayer()
    '''m.musicPlayer('../music/五月天 - 你说那 C 和弦就是....mp3')
    time.sleep(2)
    m.musicStop()'''
    st = '../music/五月天 - 你说那 C 和弦就是....mp3'
    s.count = 0
    screenController_thread = threading.Thread(target=s.screenController, args=())
    musicPlayer_thread = threading.Thread(target=m.musicPlayer, args=(st,))
    controller_thread = threading.Thread(target=c.controllerThread,args=())
    controller_thread.start()
    screenController_thread.start()
    musicPlayer_thread.start()
    #time.sleep(100)
    #s.count = 100
    # m.isStop = True
    # m.musicStop()
    
    
