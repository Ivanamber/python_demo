from doctest import set_unittest_reportflags
from encodings import utf_8

import numpy as np
import pandas as pd
from ctypes import *
import sys
import time
import re
import math
#测试数据的起始列
COL = 11

#解析excel 函数

def trans_excel_func(str, Senddata, Factor, Offset):
    if(re.search(r"FLOOR", str, re.I)):
        answer = trans_floor(str, Senddata)
    elif (re.search(r'IFS', str, re.I)):
        answer = trans_ifs(str, Senddata)
    elif(re.search(r'IF', str, re.I)):
        answer = trans_if(str, Senddata)
    elif(re.search(r'ROUND', str, re.I)):
        answer = trans_round(str, Senddata)
    elif (re.search(r'INT', str, re.I)):
        answer = trans_int(str, Senddata)
    else:
        answer = eval(str)
    return answer

#解析excel中FLOOR函数
def trans_floor(str, senddata):
    ans = re.findall(r"\d+\.?\d*", str)
    num1 = float(ans[1])
    num2 = float(ans[2])
    if(len(ans) > 3):
        num3 = float(ans[3])
        return FLOOR(senddata, num1, num2) * num3
    else:
        return FLOOR(senddata, num1, num2)

def FLOOR( a, b, c):
    tmp = a / b
    ans = (tmp - (tmp % c))
    return round(ans, 3)

#解析excel中IF函数
def trans_if(str, senddata):
    ans = re.findall(r"\d+\.?\d*", str)
    num1 = float(ans[1])
    num2 = float(ans[2])
    num3 = float(ans[3])
    if(len(re.findall(r'[a-z]', str, re.I)) > 3):
        return IF(str, num1, num2, senddata, senddata)
    else:
        return IF(str, num1, num2, num3, senddata)

def IF(str, num1, num2, num3, senddata):
    if(re.search(r'>=\d', str, re.I)):
        answer = num2 if senddata >= num1 else num3
    elif(re.search(r'<=\d', str, re.I)):
        answer = num2 if senddata <= num1 else num3
    elif (re.search(r'=\d', str, re.I)):
        answer = num2 if senddata == num1 else num3
    elif (re.search(r'<\d', str, re.I)):
        answer = num2 if senddata < num1 else num3
    else:
        answer = num2 if senddata > num1 else num3
    return  answer

#解析round函数
def trans_round(str, senddata):
    ans = re.findall(r"\d+\.?\d*", str)
    num = int(ans[1])
    return round(senddata, num)
#解析IFS函数
def trans_ifs(str, senddata):
    if(len(re.findall(r"\W\d+\.?\d*", str)) == len(re.findall(r"\d+\.?\d*", str))):
        ans = re.findall(r"\d+\.?\d*", str)
        for i in range(len(ans)):
            if(2*i+1 < len(ans)):
                if(float(ans[2*i]) == senddata):
                    answer = float(ans[2*i+1])
                    return answer
    else:  ## 暂时未考虑IFS中逻辑运算符不同的情况
        ans = re.findall(r"\d+\.?\d*", str)
        for i in range(len(ans)):
            if(3*i+2 < len(ans)):
                if (re.search(r'>=\d', str, re.I)):
                    if(senddata >= float(ans[3*i+1])):
                        answer = float(ans[3*i+2])
                        return answer
                elif (re.search(r'<=\d', str, re.I)):
                    if(senddata <= float(ans[3*i+1])):
                        answer = float(ans[3*i+2])
                        return answer
                elif (re.search(r'=\d', str, re.I)):
                    if(senddata == float(ans[3*i+1])):
                        answer = float(ans[3*i+2])
                        return answer
                elif (re.search(r'<\d', str, re.I)):
                    if(senddata < float(ans[3*i+1])):
                        answer = float(ans[3*i+2])
                        return answer
                else:
                    if(senddata > float(ans[3*i+1])):
                        answer = float(ans[3 * i + 2])
                        return answer
    return 0

def trans_int(str, senddata):
    num = len(re.findall(r'INT', str, re.I))
    ans_num = re.findall(r"\d+\.?\d*", str)
    ans_lo = re.findall(r'[-+*/]', str, re.I)
    for i in range(num):
        if(ans_lo[i] == '+'):
            answer = math.floor(senddata + float(ans_num[i+1]))
        elif(ans_lo[i] == '-'):
            answer = math.floor(senddata - float(ans_num[i+1]))
        elif (ans_lo[i] == '*'):
            answer = math.floor(senddata * float(ans_num[i+1]))
        elif (ans_lo[i] == '/'):
            answer = math.floor(senddata / float(ans_num[i+1]))
        senddata = answer
    return answer

def load_csv(path):
    csv_data = pd.read_csv(path, encoding='gbk')
    FrameData = pd.DataFrame(csv_data)
    ## csv测试集补全，测试集第一行的值必须有，根据该值补全，例如某列senddata第一行值为1，其余各行值为空，则表示该列值与第一列senddata相同
    for i in range(FrameData.shape[1] - COL):
        if(FrameData.iloc[1, COL + i] != FrameData.iloc[1, COL + i]): ##值为nan
            index = int(FrameData.iloc[0, COL + i])
            FrameData.iloc[:, COL + i] = FrameData.iloc[:, COL + index - 1]
        # print(FrameData.iloc[:, COL + i])
    return FrameData

def database_init():
    class SubStruct_list(Structure):
        _fields_ = [("name", c_char * 45),
                    ("enable", c_ubyte),
                    ("value_send", c_double),
                    ("value_rcv", c_double),
                    ("value_want", c_double),
                    ("errrange", c_float)]
        def __init__(self):
            self.name[45] = 0
            self.enable = 0
            self.value_send = 0
            self.value_rcv = 0
            self.value_want = 0
            self.errrange = 0

    class FathStruct_list(Structure):
        _fields_ = [("count", c_uint),
                    ("SignalArry", SubStruct_list * 500)]

        def __init__(self):
            self.count = 0

    DataBase = FathStruct_list()
    return DataBase

def send_data(FrameData, DataBase):
    # 遍历所有Senddata列
    for j in range(FrameData.shape[1] - COL):
        # 遍历所有行
        for i in range(FrameData.shape[0]):
            Factor = FrameData['理论值factor'][i]
            Senddata = FrameData.iloc[i, COL + j]
            Offset = FrameData['理论值offset'][i]
            DataBase.count = i
            DataBase.SignalArry[i].enable = FrameData['0不测试 1测试'][i]
            DataBase.SignalArry[i].value_send = Senddata
            str = FrameData['MAF获取理论值'][i]
            DataBase.SignalArry[i].value_want = trans_excel_func(str, Senddata, Factor, Offset)
            DataBase.SignalArry[i].errrange = FrameData['允许误差%'][i]
            DataBase.SignalArry[i].name = bytes(FrameData['共享内存内部信号'][i], encoding='utf-8')
            print(j, "value_want:",DataBase.SignalArry[i].value_want)
            # print(j, DataBase.count, DataBase.SignalArry[i].name, DataBase.SignalArry[i].enable,
            #       DataBase.SignalArry[i].value_send, "value_want:", DataBase.SignalArry[i].value_want,
            #       DataBase.SignalArry[i].errrange)
        # 调用C接口
        # target.fg_SSPApp_SetDateToDB(byref(DataBase))
        # print("num:", j, "send to shm")
        # 延时
        time.sleep(1)

def main():
    # target = cdll.LoadLibrary("libsspshm.so")
    # target.fl_SSP_InitDB()  # 调用c中的初始化函数
    FrameData = load_csv('CSVtoSSP.csv')
    DataBase = database_init()
    #
    send_data(FrameData, DataBase)

    print(FrameData['MAF获取理论值'][8])
    # print(DataBase)
    # print(DataBase.count)
    # print(DataBase.SignalArry[i].enable)
    # print(DataBase.SignalArry[i].name)
    # print(DataBase.SignalArry[i].value_send)
    # print(DataBase.SignalArry[i].value_want)
    # print(DataBase.SignalArry[i].errrange)



if __name__ == '__main__':
    main()
