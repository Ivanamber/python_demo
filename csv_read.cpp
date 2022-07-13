#include <stdio.h>
#include <memory.h>
#include <stdlib.h>
#include <string.h>
#include "SSP_sharedmem.hpp"

int main()
{

FILE *fp = NULL;

char *line,*record;
char buffer[2048];
char *line_buf[32];

/*
struct SIGNAL
{
	char name[50];     // signal name 
	unsigned char enable;       // signal check enable 
	double value_send;          // send value
	double value_rcv;           // rcv value
	double value_want;           // rcv want
	float errrange;             // err range
};
struct SHM_DB_ST
{
    struct SIGNAL SignalArry [100];
    unsigned int count;         //signal num
};
*/

struct SHM_DB_ST DataBase;

if((fp = fopen("ssp_testcase.csv", "rb")) != NULL)
{
    printf("success find ssp_testcase.csv\n");   
    
    fseek(fp, 0L, SEEK_SET);  //定位到第二行，每个英文字符大小为1
    int j = 0;
    unsigned int line_cnt = 0;

    //read first line
    line = fgets(buffer, sizeof(buffer), fp);
    record = strtok(line, ",");
    while (j < 12)//读取每一行的数据
    {
        line_buf[j] = record;
        record = strtok(NULL, ",");
        j++;
    }
    //read data
    while ((line = fgets(buffer, sizeof(buffer), fp))!=NULL)//当没有读取到文件末尾时循环继续
    {
        j = 0;
        record = strtok(line, ",");
        while (j < 12)//读取每一行的数据
        {
            line_buf[j] = record;
            //printf("%d-%-10s ",j,line_buf[j]);
            record = strtok(NULL, ",");
            j++;
        }

        strcpy(DataBase.SignalArry[line_cnt].name,line_buf[3] );
        DataBase.SignalArry[line_cnt].enable = *line_buf[10] - '0';
        DataBase.SignalArry[line_cnt].value_send = strtod(line_buf[5],NULL);
        DataBase.SignalArry[line_cnt].value_want = strtod(line_buf[8],NULL);
        DataBase.SignalArry[line_cnt].errrange   = strtod(line_buf[9],NULL);
        line_cnt++;
        //printf("%-40s \t%d \t%lf \t%lf \t%f\n",DataBase.SignalArry[j].name,DataBase.SignalArry[j].enable,DataBase.SignalArry[j].value_send,DataBase.SignalArry[j].value_want,DataBase.SignalArry[j].errrange);
    } 

    for(int k =0;k<line_cnt;k++)//当没有读取到文件末尾时循环继续
    {
        printf("%-40s \t%d \t%lf \t%lf \t%f\n",DataBase.SignalArry[k].name,DataBase.SignalArry[k].enable,DataBase.SignalArry[k].value_send,DataBase.SignalArry[k].value_want,DataBase.SignalArry[k].errrange);
    } 
    
    printf("test case number is %d\n",line_cnt);
    
    DataBase.count = line_cnt;
    fg_SSPApp_SetDateToDB(&DataBase);
    printf("test case number xxxxxxxxxxxxxx is %d\n",DataBase.count);    
    fclose(fp);
    fp = NULL;
}
else
{
    printf("error!!!!!!!! no csv\n");
    printf("can not find ssp_testcase.csv\n");    
}

}