/************************************************
copyright:none
filename: sharedmem_init.cpp
description: shared memorary functions
author: wumingghao
version:v1.0
*************************************************/
#include <stdio.h>
#include <stdlib.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <string.h>
#include "SSP_sharedmem.hpp"
#include <unistd.h>
#include <pthread.h>
using namespace std;
/*-------------------------------------------------------*/
unsigned char str_rt[10];
/************************************************
function name :fl_SSP_InitDB
description: initialize shared memorary of DataBase
input: none
output:none
*************************************************/
void fl_SSP_InitDB()
{
    int shm_id;

    printf("create share memory size is %ld\r\n",SHM_DB_Size);
    key_t key=ftok("/tmp",1);
    shm_id = shmget(key, SHM_DB_Size,IPC_CREAT|0666);        //creat
    if(shm_id == -1)
    {
        printf("create share memory fail!\r\n");
        exit(1);
    }
}

/************************************************
function name :fg_SSPApp_GetDateFromDB
description: get date frome shared memorary of DataBase
input: signal--> name of signal      value
output:none
*************************************************/  
struct SHM_DB_ST readptr1;
struct SHM_DB_ST * fg_SSPApp_GetDateFromDB()
{
    int shm_id,flag;
    
    struct SHM_DB_ST *DataBase;
    pthread_mutex_t * sharedLock;
    struct shmid_ds buf ;
    //char *DataBase;
   
    key_t key=ftok("/tmp",1);
    shm_id = shmget(key, SHM_DB_Size,0);
    if(shm_id == -1)
    {
        printf("create share memory fail!\r\n");
        exit(1);
    }
    flag = shmctl( shm_id, IPC_STAT, &buf) ;
    DataBase = (struct SHM_DB_ST *) shmat(shm_id, NULL, 0);
    if(DataBase == (void*)-1)
    {
        printf("shmat err!\r\n");
        exit(1);
    }
    //sharedLock = (pthread_mutex_t *)DataBase; 
/*读数据前查看是否上锁*/    
    //printf("read begain\r\n");
    //pthread_mutex_lock(sharedLock);
    //printf("read over\r\n");
    memcpy(&readptr1, DataBase, SHM_DB_Size);
    // readptr->count = DataBase->count;
    // readptr->SignalArry[1].name = DataBase->SignalArry[1].name;
/*读完数据解锁*/
    //pthread_mutex_unlock(sharedLock);
    shmdt(DataBase);
    return &readptr1;
} 
// struct SHM_DB_ST * fg_SSPApp_GetDateFromDB()
// {
//     int shm_id;
//     struct SHM_DB_ST *readptr;
//     struct SHM_DB_ST *DataBase;
//     pthread_mutex_t * sharedLock;
//     key_t key=ftok("/tmp",1);
//     shm_id = shmget(key, SHM_DB_Size,0);
//     if(shm_id == -1)
//     {
//         printf("create share memory fail!\r\n");
//         exit(1);
//     }
//     DataBase = (struct SHM_DB_ST *) shmat(shm_id, NULL, 0);
//     if(DataBase == (void *)-1)
//     {
//         printf("shmat err!\r\n");
//         exit(1);
//     }
// //     sharedLock = (pthread_mutex_t *)DataBase;  
// // /*读数据前查看是否上锁*/
// //     pthread_mutex_lock(sharedLock);  
//     //ptr = *DataBase;
//     // printf("read shared len %ld\r\n",SHM_DB_Size);
//     // printf("11 %s\r\n",DataBase->SignalArry[0].name);
//     // printf("11 %s\r\n",DataBase->SignalArry[1].name);
//     memcpy(readptr, DataBase, SHM_DB_Size);
//     printf("copy ok \r\n");

// /*读完数据解锁*/
//     //pthread_mutex_unlock(sharedLock);    
//     if(shmdt(DataBase) < 0)
//     {
//         printf("shmdt err!\r\n");
//         exit(1);        
//     }
//     printf("mdt end\r\n");
//     //printf("11 %s\r\n",DataBase->SignalArry[1].name);
//     //printf("sharedmem get signal %s : %s\r\n",&signal_name[signal][0], str.c_str());    
//     return 0;
// }  

/************************************************
function name :fg_SSPApp_SetDateToDBA
description: get date frome shared memorary of DataBase
input: signal--> name of signal      value
output:none
*************************************************/ 

void fg_SSPApp_SetDateToDB(struct SHM_DB_ST* src)
{
    int shm_id;
    struct SHM_DB_ST *DataBase;
    pthread_mutex_t * sharedLock;
	pthread_mutexattr_t ma;
    key_t key=ftok("/tmp",1);
    shm_id = shmget(key, SHM_DB_Size,0);
    if(shm_id == -1)
    {
        printf("create share memory fail!\r\n");
        exit(1);
    }
    DataBase = (struct SHM_DB_ST *) shmat(shm_id, NULL, 0);
    if(DataBase == (void *)-1)
    {
        printf("shmat err!\r\n");
        exit(1);
    }
//      sharedLock = (pthread_mutex_t *)DataBase;
// /*初始化锁*/    
//     pthread_mutexattr_init(&ma);
//     pthread_mutexattr_setpshared(&ma, PTHREAD_PROCESS_SHARED);
//     pthread_mutexattr_setrobust(&ma, PTHREAD_MUTEX_ROBUST);
//     pthread_mutex_init(sharedLock,&ma);
// /*写数据前上锁*/
//      pthread_mutex_lock(sharedLock);
    memcpy(DataBase, src, SHM_DB_Size);
    //printf("sharedmem set signal %s : %s\r\n", &signal_name[signal][0], value);
/*写完数据解锁*/    
    
    //pthread_mutex_unlock(sharedLock);
    if(shmdt(DataBase) < 0)
    {
        printf("shmdt err!\r\n");
        exit(1);        
    }
    
}
/************************************************
function name :fg_SSPApp_RmDB
description: remove sharedmemorary of DB__APP
input: none
output:none
*************************************************/ 
void fg_SSPApp_RmDB()
{
    int shm_id;
    string str;

    printf("rm share memory DBAPP\r\n");
    key_t key=ftok("/tmp",1);
    shm_id = shmget(key, SHM_DB_Size,0);
    if(shm_id == -1)
    {
        printf("create share memory fail!\r\n");
        exit(1);
    }   
    if (shmctl(shm_id, IPC_RMID, 0) == -1)  
    {
        printf("shmctl err!\r\n");
    }
    
}    

int main1()
{
    struct SHM_DB_ST DataBase;
    fl_SSP_InitDB();
    strcpy((char *)DataBase.SignalArry[1].name, "ESP"); 
    DataBase.SignalArry[1].enable = 1;
    DataBase.SignalArry[1].value_send = 49.01;
    DataBase.SignalArry[1].value_rcv = 50.02;
    DataBase.SignalArry[1].errrange = 0.1; 
    fg_SSPApp_SetDateToDB(&DataBase);
    printf("success! %s\r\n",DataBase.SignalArry[1].name);
    //fg_SSPApp_RmDB();
    // DataBase = *fg_SSPApp_GetDateFromDB();  
    // printf("get date %s\r\n",DataBase.SignalArry[1].name);
}

int main()
{
    struct SHM_DB_ST DataBase;
    DataBase = *fg_SSPApp_GetDateFromDB();
    for (int i = 0; i < 10; i++){

        printf("get date %s\r\n",DataBase.SignalArry[i].name);
        printf("get date %d\r\n",DataBase.SignalArry[i].enable);
        printf("get date %f\r\n",DataBase.SignalArry[i].value_send);
        printf("get date %f\r\n",DataBase.SignalArry[i].value_rcv);
        printf("get date %f\r\n",DataBase.SignalArry[i].errrange);
        //fg_SSPApp_RmDB();
        sleep(1);
        printf("num:", i, "\r\n");
    }
    return 0;
}
