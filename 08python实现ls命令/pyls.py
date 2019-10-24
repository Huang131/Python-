'''
@Descripttion: 用python实现ls命令
@version: 0.0.1
@Author: Huang
@Date: 2019-10-24 18:55:52
@LastEditors: Huang
@LastEditTime: 2019-10-24 20:53:08
'''

import argparse
import os
import time
import prettytable

# 定义一个参数解析器
parser = argparse.ArgumentParser(
    prog='ls',
    usage='pyls.py [-h -a -r]',
    add_help=True,
    description='用python写的ls命令')  # 获取参数解析器,默认add_help就是True

# 给解析器加入位置参数path和选项参数 a和r
parser.add_argument('path', nargs='?', default='.', help='文件夹路径')
parser.add_argument('-a', '--all', action='store_true', help='列出文件夹下的文件')
parser.add_argument('-s',
                    '--sorted',
                    action='store_true',
                    help='列出按文件大小排序后的文件夹下的文件')
parser.add_argument('-t',
                    '--time',
                    action='store_true',
                    help='列出按时间排序后的文件夹下的文件')
parser.add_argument('-r',
                    '--recursion',
                    action='store_true',
                    help='循环列出文件夹下所有文件')

# 用解析器解析命令行输入的参数
args = parser.parse_args(
)  # 分析参数,空表示无参数传入，也可以带参传入，例如：args = parser.parse_args(('-r','-a','.'))

# 判断路径是否合法
directory = args.path
# 如果指定目录不存在，抛出异常
if not os.path.exists(directory):
    raise ValueError(
        f'{directory} does`t exist'
    )  # 等同于 raise ValueError('{} does`t exist'.format(directory))

# 如果directory不是一个目录，抛出异常
if not os.path.isdir(directory):
    raise ValueError(f'{directory} is not a directory')


class LsCommand(object):
    def __init__(self,
                 show_all=False,
                 directory='.',
                 recursion=False,
                 show_sorted_size=False,
                 show_sorted_time=False):
        '''
        show_all: 显示所有文件
        directory: 指定的文件目录
        recursion: 是否递归显示目录下的文件-本代码还没有实现这个
        show_sorted_size：按文件大小排序显示
        show_sorted_time：按创建时间排序显示
        '''
        self.show_all = show_all
        self.recursion = recursion
        self.directory = os.path.abspath(directory)
        self.show_sorted_size = show_sorted_size
        self.show_sorted_time = show_sorted_time

    def list_dir(self):
        '''
        os.listdir: 列出当前文件夹下面的所有文件和文件夹
        遍历目录下的文件，文件夹return文件夹的列表list_temp2和文件列表list_temp3
        '''

        list_temp2 = []
        list_temp3 = []
        file_id = 0
        if self.show_all:
            for i in os.listdir(self.directory):
                list_temp1 = []
                list_temp1.append(file_id)
                list_temp1.append(i)
                list_temp1.append(os.path.getsize(self.directory + '\\' + i))
                list_temp1.append(
                    time.strftime(
                        '%Y-%m-%d %H:%M:%S',
                        time.localtime(
                            os.stat(self.directory + '\\' + i).st_ctime)))
                file_id += 1

                if os.path.isdir(self.directory + '\\' + i):
                    list_temp2.append(list_temp1)
                else:
                    list_temp3.append(list_temp1)

        return list_temp2, list_temp3

    # 按照文件大小或者按照时间进行排序，返回排序后的文件列表
    def sorted_file(self, list_temp2, list_temp3):
        if self.show_sorted_size:
            list_temp2 = sorted(list_temp2, key=lambda x: x[2])
            list_temp3 = sorted(list_temp3, key=lambda x: x[2])

        if self.show_sorted_time:
            list_temp2 = sorted(list_temp2, key=lambda x: x[3])
            list_temp3 = sorted(list_temp3, key=lambda x: x[3])

        return list_temp2, list_temp3

    # 定义运行主函数
    def run(self):
        '''
        return所有文件或者排序后的文件列表
        '''
        list_temp2, list_temp3 = self.list_dir()
        if self.show_sorted_size or self.show_sorted_time:
            list_temp2, list_temp3 = self.sorted_file(list_temp2, list_temp3)

        return list_temp2, list_temp3


def main():
    args = parser.parse_args()
    ls = LsCommand(args.all, args.path, args.recursion, args.sorted, args.time)
    table_x = prettytable.PrettyTable(["ID", "目录名", "文件大小", "创建时间"])
    table_x.align['目录名'] = 'l'
    table_y = prettytable.PrettyTable(["ID", "文件名", "文件大小", "创建时间"])
    table_y.align['文件名'] = 'l'
    list_dir_file = ls.run()
    for i in list_dir_file[0]:
        table_x.add_row(i)

    for i in list_dir_file[1]:
        table_y.add_row(i)
    print(table_x)
    print(table_y)


if __name__ == '__main__':
    main()
