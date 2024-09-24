import time


# .-..---...-.
def readTxt():
    arrays = []
    f = open('input.txt', 'r')
    for line in f:
        arrays.append(line)

    print(len(arrays))
    return arrays

def printArray(arrays):
    for array in arrays:
        print(array.replace('\n', ''))

def secretBase():
    printArray(readTxt())
    return readTxt()
    
def checkPassword(pwd):
    password = '282288822282'
    if password == pwd:
        return True
    else:
        return False

# LRC歌词读取
def readLRC(songName):
    f = open(songName+'.txt', 'r', encoding='utf-8')
    # f = open('青空未来.txt', 'r', encoding='utf-8')
    lrcLines = f.readlines()
    dict = {}
    for line in lrcLines:
        # 时间格式默认为[mm:ss.ss]格式
        time = line[1:9]
        str = line[10:].replace('\n', '')
        dict[time] = str
    return dict


if __name__ == '__main__':
    printArray(readTxt())
