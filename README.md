# MaydayFansDemo
一个五月天相关的树莓派实验品    
目前进度：整体完成，正在细节调试中    
## 材料准备    
树莓派 * 1     
树莓派可接圆屏（触摸功能未来可能会用上）（可直接电商平台搜索单片机 圆屏，建议官方购买，比较便宜） * 1     
USB音响 * 1    
按钮 * 1（支持上下左右中键以及set和rst按钮）    

## 使用    
### 安装屏幕运行库：
这里建议用Python3，因为其他代码里用到了2和3不一样的语法    
```
git clone https://github.com/WiringPi/WiringPi
cd WiringPi
./build
gpio -v
# 运行gpio -v会出现2.70版本，如果没有出现说明安装出错

#python2
sudo apt-get update
sudo apt-get install python-pip
sudo apt-get install python-pil
sudo apt-get install python-numpy
sudo pip install RPi.GPIO
sudo pip install smbus
sudo pip install spidev
#python3
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-pil
sudo apt-get install python3-numpy
sudo pip3 install RPi.GPIO
sudo pip3 install smbus
sudo pip3 install spidev
```


### 代码下载：    
```
git clone https://github.com/CaptainDra/MaydayFansDemo.git    
```   

### 运行(如果以后仓库改名请修改此处代码)：    
```
cd MaydayFansDemo/code
sudo python main.py
```
### 设置开机自启动：    
在 /home/pi/.config 下创建一个文件夹，名称为 autostart    
```
mkdir /home/pi/.config/autostart
```
在该文件夹下创建一个xxx.desktop文件，文件名以.desktop结尾，名称可自定义，文件的内容如下(请修改exec后变成main.py路径)：    
```
[Desktop Entry]
Name=example
Comment=My Python Program
Exec=python xxxx
Terminal=false
MultipleArgs=false
Type=Application
Categories=Application;Development;
StartupNotify=true
```
P.S.:这样自动启动进程需要通过杀进程方式来关闭

## 相关链接    
显示屏说明文档：[微雪L1.28](https://www.waveshare.net/wiki/1.28inch_Touch_LCD#.E8.BF.90.E8.A1.8C.E6.B5.8B.E8.AF.95.E7.A8.8B.E5.BA.8F)       


