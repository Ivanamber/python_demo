from doctest import set_unittest_reportflags
from encodings import utf_8
import pandas as pd
from ctypes import *
import sys
import time
import re

def excel_trans(str):
    if(re.match("FLOOR", str)):
        ans = re.findall(r"\d+\.?\d*",str)
        print(ans)
        end1 = float(ans[1])
        end2 = float(ans[2])
        end3 = float(ans[3])
        return end1, end2, end3
    else:
        return 0, 0, 0






#解析excel中FLOOR函数

def FLOOR( a, b, c, d):
    tmp = a / b
    ans = (tmp - (tmp % c)) * d
    return ans


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
            DataBase.SignalArry[i].enable = FrameData['0 Untest 1 Test'][i]
            DataBase.SignalArry[i].value_send = Senddata
            # print(FrameData['Theodata'][i])
            end1, end2, end3 = excel_trans(FrameData['Theodata'][i])
            print(end1, end2, end3)
            # DataBase.SignalArry[i].value_want = eval(FrameData['Theodata'][i])
            DataBase.SignalArry[i].errrange = FrameData['errrange'][i]
            DataBase.SignalArry[i].name = bytes(FrameData['Memsig'][i], encoding='utf-8')
            # print("value_want:",DataBase.SignalArry[i].value_want)
            # print(j,DataBase.count, DataBase.SignalArry[i].name, DataBase.SignalArry[i].enable,
            #       DataBase.SignalArry[i].value_send, "value_want:",DataBase.SignalArry[i].value_want, DataBase.SignalArry[i].errrange)

        # 调用C接口
        # target.c_fg_SSPApp_SetDateToDB(byref(DataBase))

        # 延时
        time.sleep(10)
        # print(DataBase)
        # print(DataBase.count)
        # print(DataBase.SignalArry[i].enable)
        # print(DataBase.SignalArry[i].name)
        # print(DataBase.SignalArry[i].value_send)
        # print(DataBase.SignalArry[i].value_want)
        # print(DataBase.SignalArry[i].errrange)


if __name__ == '__main__':
    main()
