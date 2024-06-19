#import chardet
import os
import sys
import time
import logging
import spidev as SPI

from lib import screenPlayer

sys.path.append("..")
from lib import LCD_1inch28


screenPlayer()
screenPlayer.screenController()