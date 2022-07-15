#ifndef SHAREDMEM_INIT_H
#define SHAREDMEM_INIT_H

#include <string>
#include <pthread.h>
using namespace std;
extern "C"
{
#define MAX_COUNT            		1000
#define SHM_Signal_Size             sizeof(struct SIGNAL)
#define SHM_DB_Size             	sizeof(struct SHM_DB_ST)
struct SIGNAL
{
	char name[45];     			// signal name 
	unsigned char enable;       // signal check enable 
	double value_send;          // send value
	double value_rcv;           // rcv value
	double value_want;          // value we want
	float errrange;             // err range
};
struct SHM_DB_ST
{
	unsigned int count;         //signal num
    struct SIGNAL SignalArry [MAX_COUNT];
};
void fl_SSP_InitDB();

struct SHM_DB_ST * fg_SSPApp_GetDateFromDB();


void fg_SSPApp_SetDateToDB(struct SHM_DB_ST* src);

void fg_SSPApp_RmDB();

void Sem_open_SSP();

void Sem_post_SSP();

void Sem_unlink_SSP();
}
#endif
