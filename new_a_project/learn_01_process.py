# from random import randint
# from time import time, sleep
# from multiprocessing import Process
#
# def download_task(filename):
#     print('开始下载%s...' % filename)
#     time_to_download = randint(5, 10)
#     sleep(time_to_download)
#     print('%s下载完成! 耗费了%d秒' % (filename, time_to_download))
#
# def main():
#     start = time()
#     p1 = Process(target=download_task, args=("Python从入门到住院.pdf",))
#     p1.start()
#     p2 = Process(target=download_task, args=("Peking Hot.avi",))
#     p2.start()
#     p1.join()
#     p2.join()
#     end = time()
#     print('总共耗费了%.2f秒.' % (end - start))
#
# if __name__ == '__main__':
#     main()
#
#



# import multiprocessing
# a = 1
# def demo1():
#     global a
#     a+=1
# def demo2():
# #打印出来的值是2说明是共享的线程是共享
# # #打印结果是1进程是不共享的
#     print(a)
# def main():
#     t1 = multiprocessing.Process(target=demo1)
#     t2 = multiprocessing.Process(target=demo2)
#     t1.start()
#     t2.start()
#
#
# if __name__ == '__main__':
#     main()





# import multiprocessing as mul_p
# import time
# from random import randint, random
#
# egg1 = 6
# def write(egg2, q):
#     global egg1
#     print("write全局变量egg1[%s].."%egg1)
#     print("write入参egg2[%s].."%egg2)
#     egg1 -= 1
#     count = randint(1,8)
#     #将修改后的彩蛋1的值放入队列中去
#     q.put(egg1)
#
#
# def read(egg2, q):
#     global egg1
#     print("read全局变量egg1[%s].."%egg1)
#     print("read入参egg2[%s].."% egg2)
#     while True:
#         #从队列中取出p1子进程中的全局变量彩蛋1的值egg1
#         q.get()
#         print("read接收到的write中的全局变量egg1[1]的值：%d"%egg1)
#         if q.empty():
#             print("接收完毕..")
#             break
#
#
# def main():
#     #假设连个进程都需要打印下面这个彩蛋2
#     egg2= 2
#     #①创建一个队列，可以不填，队列就可以很大，但有个极限，我们不去考虑它
#     # #如果填了数字为×，则这个队列可以存储×个数据
#     q = mul_p.Queue()
#     #②创建两个进程对象
#     p1 = mul_p.Process(target=write, args=(egg2,q,))
#     p2 = mul_p.Process(target=read, args=(egg2,q,))
#     #③让两个子进程开始工作
#     p1.start()
#     #先让主进程休息1s让p1子进程先执行完，不然两个子进程争着执行打印输出会乱套
#     p2.start()
#
# if __name__ == '__main__':
#     main()













import time,multiprocessing
# from multiprocessing import value
def add1(value,number):
    print("start add1 number={0}".format(number.value))
    for i in range(1,5):
        number.value += value
        time.sleep(0.3)
        print("number={0}".format (number.value))
def add3(value,number):
    print("start add3 number={0}".format(number.value))
    try:
        for i in range(1,5):
            number.value += value
            time.sleep(0.3)
            print ("number={0}".format (number.value))
    except Exception as e:
        raise e

if __name__ == '__main__':
    print("star main")
    number= multiprocessing.Value('d', 0) #在内存分配一个空间 d表示数字类型，可支持的数据类型如下表#number= Array（'i'，3） #表示开辟的共享内存容量为3，当再超过3时就会报错
    p1 = multiprocessing.Process(target=add1,args=(1,number))
    p3 = multiprocessing.Process(target=add3,args=(3,number))
    p1.start()
    p1.join()
    p3.start()
    print("end main")