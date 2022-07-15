#include <fcntl.h>           /* For O_* constants */
#include <sys/stat.h>        /* For mode constants */
#include <semaphore.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
int main(){

    sem_t *sem;
    int val;
    printf("1\r\n");
    sem = sem_open("update_check", O_EXCL, 0777, 0);
    if(sem == (sem_t *) SEM_FAILED){
        printf("error\r\n");
        return 0;
    }
    printf("create\r\n");
//    sem_init(sem,0,1);
    sem_post(sem);
//    printf("post\r\n");
    sem_getvalue(sem, &val);
    printf("val:%d\n", val);
    sleep(2);

    sem_close(sem);
    sem_unlink("update_check");
//    if(val == 1){
//        printf("get sem from python\r\n");
//
//    }

    return 0;
}