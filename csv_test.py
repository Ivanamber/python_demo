from doctest import set_unittest_reportflags
from encodings import utf_8
import threading
import numpy as np
import pandas as pd
from ctypes import *
import sys
import time
import re
import math
#测试数据的起始列
COL = 12
#保留小数点位数
Decimals = 5
#解析excel 函数

def trans_excel_func(exec_str, Senddata, Factor, Offset):
    if(re.search(r"FLOOR", exec_str, re.I)):
        answer = round(trans_floor(exec_str, Senddata), Decimals)
    elif (re.search(r'IFS', exec_str, re.I)):
        answer = round(trans_ifs(exec_str, Senddata), Decimals)
    elif(re.search(r'IF', exec_str, re.I)):
        answer = round(trans_if(exec_str, Senddata), Decimals)
    elif(re.search(r'ROUND', exec_str, re.I)):
        answer = round(trans_round(exec_str, Senddata), Decimals)
    elif (re.search(r'INT', exec_str, re.I)):
        answer = round(trans_int(exec_str, Senddata), Decimals)
    else:
        answer = eval(exec_str)
        ans_str = str(answer)
        if(answer % 1 != 0):
            if(len(ans_str.split(".")[1]) >= 5):
                answer = round(answer, Decimals)
    return answer

#解析excel中FLOOR函数
def trans_floor(exec_str, senddata):
    ans = re.findall(r"\d+\.?\d*", exec_str)
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
def trans_if(exec_str, senddata):
    ans = re.findall(r"\d+\.?\d*", exec_str)
    num1 = float(ans[1])
    num2 = float(ans[2])
    num3 = float(ans[3])
    if(len(re.findall(r'[a-z]', exec_str, re.I)) > 3):
        return IF(exec_str, num1, num2, senddata, senddata)
    else:
        return IF(exec_str, num1, num2, num3, senddata)

def IF(exec_str, num1, num2, num3, senddata):
    if(re.search(r'>=\d', exec_str, re.I)):
        answer = num2 if senddata >= num1 else num3
    elif(re.search(r'<=\d', exec_str, re.I)):
        answer = num2 if senddata <= num1 else num3
    elif (re.search(r'=\d', exec_str, re.I)):
        answer = num2 if senddata == num1 else num3
    elif (re.search(r'<\d', exec_str, re.I)):
        answer = num2 if senddata < num1 else num3
    else:
        answer = num2 if senddata > num1 else num3
    return  answer

#解析round函数
def trans_round(exec_str, senddata):
    ans = re.findall(r"\d+\.?\d*", exec_str)
    num = int(ans[1])
    return round(senddata, num)
#解析IFS函数
def trans_ifs(exec_str, senddata):
    if(len(re.findall(r"\W\d+\.?\d*", exec_str)) == len(re.findall(r"\d+\.?\d*", exec_str))):
        ans = re.findall(r"\d+\.?\d*", exec_str)
        for i in range(len(ans)):
            if(2*i+1 < len(ans)):
                if(float(ans[2*i]) == senddata):
                    answer = float(ans[2*i+1])
                    return answer
    else:  ## 暂时未考虑IFS中逻辑运算符不同的情况
        ans = re.findall(r"\d+\.?\d*", exec_str)
        for i in range(len(ans)):
            if(3*i+2 < len(ans)):
                if (re.search(r'>=\d', exec_str, re.I)):
                    if(senddata >= float(ans[3*i+1])):
                        answer = float(ans[3*i+2])
                        return answer
                elif (re.search(r'<=\d', exec_str, re.I)):
                    if(senddata <= float(ans[3*i+1])):
                        answer = float(ans[3*i+2])
                        return answer
                elif (re.search(r'=\d', exec_str, re.I)):
                    if(senddata == float(ans[3*i+1])):
                        answer = float(ans[3*i+2])
                        return answer
                elif (re.search(r'<\d', exec_str, re.I)):
                    if(senddata < float(ans[3*i+1])):
                        answer = float(ans[3*i+2])
                        return answer
                else:
                    if(senddata > float(ans[3*i+1])):
                        answer = float(ans[3 * i + 2])
                        return answer
    return 0

def trans_int(exec_str, senddata):
    num = len(re.findall(r'INT', exec_str, re.I))
    ans_num = re.findall(r"\d+\.?\d*", exec_str)
    ans_lo = re.findall(r'[-+*/]', exec_str, re.I)
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
    # csv_data = pd.read_excel(path)
    FrameData = pd.DataFrame(csv_data)
    ## csv测试集补全，测试集第一行的值必须有，根据该值补全，例如某列senddata第一行值为1，其余各行值为空，则表示该列值与第一列senddata相同
    for i in range(FrameData.shape[1] - COL):
        if(FrameData.iloc[1, COL + i] != FrameData.iloc[1, COL + i]): ##值为nan
            index = int(FrameData.iloc[0, COL + i])
            FrameData.iloc[:, COL + i] = FrameData.iloc[:, COL + index - 1]
        # print(FrameData.iloc[:, COL + i])
    return FrameData

def test_trans(FrameData, Data):
    for i in range(FrameData.shape[0]):
        if(Data.SignalArry[i].value_want != FrameData["MAF获取理论值真值"][i]):
            print(i, Data.SignalArry[i].value_want, FrameData["MAF获取理论值真值"][i])
            print('处理失败！！！\r\n')
    print('处理成功！！！\r\n')
def database_init(len):
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
                    ("SignalArry", SubStruct_list * len)]

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
            exec_str = FrameData['MAF获取理论值'][i]
            DataBase.SignalArry[i].value_want = trans_excel_func(exec_str, Senddata, Factor, Offset)
            DataBase.SignalArry[i].errrange = FrameData['允许误差%'][i]
            DataBase.SignalArry[i].name = bytes(FrameData['共享内存内部信号'][i], encoding='utf-8')

            # print(j, i, "value_want:",DataBase.SignalArry[i].value_want)
            # print(j, DataBase.count, DataBase.SignalArry[i].name, DataBase.SignalArry[i].enable,
            #       DataBase.SignalArry[i].value_send, "value_want:", DataBase.SignalArry[i].value_want,
            #       DataBase.SignalArry[i].errrange)
        # 调用C接口
        # target.fg_SSPApp_SetDateToDB(byref(DataBase))
        print("num:", j, "send to shm")
        update_check.release()
        # 延时
        time.sleep(1)
    return DataBase

def main():
    # target = cdll.LoadLibrary("libsspshm.so")
    # target.fl_SSP_InitDB()  # 调用c中的初始化函数
    update_check.release()
    # FrameData = load_csv('CSVtoSSP.csv')
    FrameData = load_csv('CSVtoSSP_lianhuashan.csv')
    DataBase = database_init(FrameData.shape[0])
    #
    Data = send_data(FrameData, DataBase)

    # print(FrameData['发送信号值'][60] * 1000 + 0)

    # 与excel处理真值做对比
    test_trans(FrameData, Data)



    # print(DataBase)
    # print(DataBase.count)
    # print(DataBase.SignalArry[i].enable)
    # print(DataBase.SignalArry[i].name)
    # print(DataBase.SignalArry[i].value_send)
    # print(DataBase.SignalArry[i].value_want)
    # print(DataBase.SignalArry[i].errrange)



if __name__ == '__main__':
    update_check = threading.Semaphore(value=0)
    main()
