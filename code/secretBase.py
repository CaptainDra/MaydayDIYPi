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

if __name__ == '__main__':
    printArray(readTxt())
