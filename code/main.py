# import chardet
import os
import queue
import sys
import time
import logging
import spidev as SPI
import pygame
import threading
import RPi.GPIO as GPIO

sys.path.append("..")
from lib import LCD_1inch28
from PIL import Image, ImageDraw, ImageFont
import secretBase

character = 2
round = 0
count = 0
musicSwitch = False
musicName = ''


# 切换角色 右移一位
def changeRightCharacter():
    global character
    global round
    character = character + 1
    if(character >= 5):
        character = character % 5
        round = round + 1


# 切换角色 左移一位
def changeLeftCharacter():
    global character
    character = (character + 5 - 1) % 5


# 屏幕类
class screenPlayer():
    # 初始化引脚设置
    def __init__(self):
        self.disp = LCD_1inch28.LCD_1inch28()
        # Initialize library.
        self.disp.Init()
        # Clear display.
        self.disp.clear()
        # Set the backlight to 100
        self.disp.bl_DutyCycle(50)
        # Create blank image for drawing.
        # 按照舞台顺序
        self.ball = ['Monster', 'Masa', 'Ashin', 'Stone', 'Ming']
        # 想加表情，但是没有艺术细胞
        self.action = [['base'],['base'],['base'],['base'],['base']]
        self.arrays = []

    def screenPlayer(self, character, mov, state):
        try:
            imageLoc = '../pic/' + character + '/' + mov + state + '.png'
            image = Image.open(imageLoc)
            self.disp.ShowImage(image)
        except IOError as e:
            logging.info(e)

    def showSongName(self):
        image1 = Image.new("RGB", (self.disp.width, self.disp.height), "BLACK")
        draw = ImageDraw.Draw(image1)
        Font1 = ImageFont.truetype("../Font/Font01.ttf", 25)
        Font2 = ImageFont.truetype("../Font/Font01.ttf", 35)
        Font3 = ImageFont.truetype("../Font/Font02.ttf", 32)
        global musicName
        text = musicName
        draw.text((20, 120), text, fill="WHITE", font=Font3)
        self.disp.ShowImage(image1)
        return

    def showSentence(self,s1,s2):
        image1 = Image.new("RGB", (self.disp.width, self.disp.height), "BLACK")
        draw = ImageDraw.Draw(image1)
        Font1 = ImageFont.truetype("../Font/Font01.ttf", 25)
        Font2 = ImageFont.truetype("../Font/Font01.ttf", 35)
        Font3 = ImageFont.truetype("../Font/Font02.ttf", 32)
        draw.text((50, 40), s1, fill="WHITE", font=Font3)
        draw.text((80, 200), s2, fill="WHITE", font=Font3)
        self.disp.ShowImage(image1)
        return

    def module_exit(self):
        self.disp.module_exit()
        logging.info("quit:")

    # 屏幕控制循环
    def screenController(self):
        try:
            global count
            count = 0
            while True:
                if len(self.arrays) > 0:
                    s1 = self.arrays.pop(0)
                    s2 = ''
                    if len(self.arrays) > 0:
                        s2 = self.arrays.pop(0)
                    self.showSentence(s1,s2)
                    time.sleep(5)
                    continue
                if count < 0:
                    time.sleep(1)
                    continue
                if count < 5:
                    count += 1
                    time.sleep(1)
                    self.showSongName()
                    continue
                sec = 0.2
                for i in range(5):
                    if count < 5:
                        continue
                    state = 'D' + str(i)
                    num = len(self.action[character])
                    self.screenPlayer(self.ball[character], self.action[character][round%num], state)
                    time.sleep(sec)
                    if (i >= 2):
                        sec = sec * 5
                    else:
                        sec = sec * 0.2
                sec = 0.2
                for i in range(5):
                    if count < 5:
                        continue
                    state = 'D' + str(4 - i)
                    num = len(self.action[character])
                    self.screenPlayer(self.ball[character], self.action[character][round%num], state)
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
        self.musicDict = {}
        self.queue = []
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.2)
        self.index = 1

    # 初始化音乐目录
    def logInit(self):
        filenames = os.listdir('../music')
        for filename in filenames:
            print(filename)
            number = ''
            for ch in filename:
                if ch == '.':
                    break
                else:
                    number += ch
            print(number)
            self.musicDict[number] = filename
            self.queue.append(number)

    def playNext(self):
        # number = self.queue.pop()
        number = self.index
        pygame.mixer.music.stop()
        self.musicPlayer('../music/' + self.musicDict[str(number)])
        global musicName
        musicName = self.musicDict[str(number)]
        musicName = musicName.replace(str(number) + '.', '')
        musicName = musicName.replace('.mp3', '')
        print(musicName)
        self.index += 1

    def musicPlayer(self, music):
        pygame.mixer.music.load(music)
        # 不自动设置音量
        # pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play()

    # 重播才有的彩蛋哦
    def musicReset(self):
        self.index = 0
        self.playNext()


# 总按钮控制器
class controller():
    screen = None
    music = None

    def __init__(self):
        self.record = queue.Queue()
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
            # 检测是否在播放音乐然后自动播放
            if pygame.mixer.music.get_busy():
                time.sleep(1)
                continue
            elif self.music.index < 40:
                self.music.playNext()
            time.sleep(1)
            continue

    def keyCallback(self, key):
        global count
        if key == self.button_up:
            volume = pygame.mixer.music.get_volume()
            pygame.mixer.music.set_volume(min(volume + 0.1, 1))
            print('提升音量')
            self.record.put('8')
        elif key == self.button_down:
            volume = pygame.mixer.music.get_volume()
            pygame.mixer.music.set_volume(max(volume - 0.1, 0))
            print('降低音量')
            self.record.put('2')
        elif key == self.button_left:
            changeLeftCharacter()
            print('左切视角')
            self.record.put('4')
        elif key == self.button_right:
            changeRightCharacter()
            print('右切视角')
            self.record.put('6')
        elif key == self.button_mid:
            count = 0
            self.midButtonCallback(self.music)
            print('切换音乐')
            self.record.put('5')
        elif key == self.button_set:
            if count >= 0:
                count = -100
                pygame.mixer.music.pause()
                print('停止运动，音乐暂停')
            else:
                count = 5
                pygame.mixer.music.unpause()
                print('音乐继续')
            self.record.put('1')
        elif key == self.button_rst:
            elements = []
            password = ''
            while not self.record.empty():
                elements.append(self.record.get())
            for element in elements:
                password += element
                self.record.put(element)
            print(password)
            if secretBase.checkPassword(password):
                self.screen.arrays = secretBase.secretBase()
                self.music.index = 99
                self.midButtonCallback(self.music)
            else:
                self.rstButtonCallback(self.music)
            print('rst')
            self.record.put('3')
        if self.record.qsize() > 12:
            self.record.get()
        time.sleep(1)

    def midButtonCallback(self, musicController):
        musicController.playNext()

    def rstButtonCallback(self, musicController):
        musicController.musicReset()


if __name__ == "__main__":
    c = controller()
    s = screenPlayer()
    m = musicPlayer()
    m.logInit()
    c.screen = s
    c.music = m
    s.count = 0
    screenController_thread = threading.Thread(target=s.screenController, args=())
    controller_thread = threading.Thread(target=c.controllerThread, args=())
    controller_thread.start()
    screenController_thread.start()

