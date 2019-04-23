# -*- coding=utf-8 -*-
from PIL import Image
import argparse

#构建命令行输入参数处理ArgumentPrase 实例
parse = argparse.ArgumentParser()

#定义输入文件、输出文件、输出字符画的宽和高
parse.add_argument('file')   #输入文件
parse.add_argument('-o','--output')  #输出文件
parse.add_argument('--width',type = int, default = 80) #输出字符画宽
parse.add_argument('--height',type = int, default = 80) #输出字符画高

#解析参数
args = parse.parse_args()

#输入的图片路径
ImgPath = args.file

#输入的字符画的宽度
ImgWidth = args.width

#输入的字符画的高度
ImgHeight = args.height

#输出字符画的路径
ImgOut = args.output

#字符集
ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

#将灰度值映射到字符上
def get_char(r,g,b,alpha = 256):
    #判断alpha值
    if alpha == 0:
        return ' '
    #获取字符集的长度
    length = len(ascii_char)

    #将RGB值转为灰度值gray,灰度值范围为0-255
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

    #灰度值映射到指定字符
    unit= (256.0+1)/length

    #返回灰度值对应的字符
    return ascii_char[int(gray/unit)]


if __name__ == '__main__':

    #打开并调整图片的宽和高
    im = Image.open(ImgPath)
    im = im.resize((ImgWidth,ImgHeight),Image.NEAREST)

    #初始化输出的字符串
    txt = ""

for i in range(ImgHeight):
    for j in range(ImgWidth):
        txt +=get_char(*im.getpixel((j,i)))
    txt +='\n'    
print(txt)

#字符画输出到文件
if ImgOut:
    with open(ImgOut,'w') as f:
        f.write(txt)
else:
    with open('output.txt','w') as f:
         f.write(txt)

