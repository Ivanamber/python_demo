from doctest import set_unittest_reportflags
from encodings import utf_8
import pandas as pd
from ctypes import *
import sys
import time
import re

def excel_trans(str, senddata, factor, offset):
    if(re.match(r"FLOOR", str, re.I)):
        ans = re.findall(r"\d+\.?\d*",str)
        num1 = float(ans[1])
        num2 = float(ans[2])
        num3 = float(ans[3])
        return FLOOR(senddata, num1, num2, num3)

    elif(re.match(r"factor \S senddata \S offset", str, re.I)):
        return fac_offset(senddata, offset, factor)
    elif(re.match(r"senddata\Z", str, re.I)):
        return stright_pass(senddata)
    else:
        return 0

def trans_floor(str, senddata):
    ans = re.findall(r"\d+\.?\d*", str)
    num1 = float(ans[1])
    num2 = float(ans[2])
    num3 = float(ans[3])
    return FLOOR(senddata, num1, num2, num3)

#解析excel中FLOOR函数

def FLOOR( a, b, c, d):
    tmp = a / b
    ans = (tmp - (tmp % c)) * d
    return round(ans, 3)

def fac_offset(senddata, offset, factor):
    return senddata * factor + offset

def stright_pass(senddata):
    return senddata


def main():
    # target = cdll.LoadLibrary("SSP_sharedmem.so")
    # target.c_fl_SSP_InitDB()  # 调用c中的初始化函数
    csv_data = pd.read_csv('CSVtoSSP.csv',encoding='gbk')
    FrameData = pd.DataFrame(csv_data)

    class SubStruct_list(Structure):
        _fields_ = [("name", c_char * 45),
                    ("enable", c_ubyte),
                    ("value_send", c_double),
                    ("value_rcv", c_double),
                    ("value_want", c_double),
                    ("errrange", c_float)]
        # def __init__(self):
        #     self.name[45] = 0
        #     self.enable = 0
        #     self.value_send = 0
        #     self.value_rcv = 0
        #     self.value_want = 0
        #     self.errrange = 0

    class FathStruct_list(Structure):
        _fields_ = [("count", c_uint),
                    ("SignalArry", SubStruct_list * 500)]

        # def __init__(self):
        #     self.count = 0
        #     self.SignalArry = 0

    DataBase = FathStruct_list()

    # 遍历所有Senddata列
    for j in range(FrameData.shape[1] - 11):
        # 遍历所有行
        for i in range(FrameData.shape[0]):
            Factor = FrameData['Factor'][i]
            Senddata = FrameData.iloc[i, 11 + j]
            Offset = FrameData['Offset'][i]
            DataBase.count = i
            DataBase.SignalArry[i].enable = FrameData['0不测试 1测试'][i]
            DataBase.SignalArry[i].value_send = Senddata
            str = FrameData['MAF获取理论值'][i];
            # print(FrameData['Theodata'][i])
            # DataBase.SignalArry[i].value_want = excel_trans(FrameData['Theodata'][i], Senddata, Factor, Offset)

            if(re.match(r"FLOOR", str, re.I)):
                DataBase.SignalArry[i].value_want = trans_floor(str, Senddata)
            else:
                DataBase.SignalArry[i].value_want = eval(FrameData['MAF获取理论值'][i])

            DataBase.SignalArry[i].errrange = FrameData['允许误差%'][i]
            DataBase.SignalArry[i].name = bytes(FrameData['共享内存内部信号'][i], encoding='utf-8')
            # print(j, "value_want:",DataBase.SignalArry[i].value_want)
            print(j,DataBase.count, DataBase.SignalArry[i].name, DataBase.SignalArry[i].enable,
                  DataBase.SignalArry[i].value_send, "value_want:",DataBase.SignalArry[i].value_want, DataBase.SignalArry[i].errrange)

        # 调用C接口
        # target.c_fg_SSPApp_SetDateToDB(byref(DataBase))

        # 延时
        time.sleep(1)
        # print(DataBase)
        # print(DataBase.count)
        # print(DataBase.SignalArry[i].enable)
        # print(DataBase.SignalArry[i].name)
        # print(DataBase.SignalArry[i].value_send)
        # print(DataBase.SignalArry[i].value_want)
        # print(DataBase.SignalArry[i].errrange)


if __name__ == '__main__':
    main()
