from urllib import request
import json
import time
import threading
import random

headers = {"Content-Type":'application/json'}
temp_data = [8.2210e-02,2.2000e+01,5.8600e+00,0.0000e+00,4.3100e-01,6.9570e+00,6.8000e+00,8.9067e+00,7.0000e+00,3.3000e+02,1.9100e+01,3.8609e+02,3.5300e+00]
raw_data = {'data':temp_data}
data = json.dumps(raw_data)
data = bytes(data, 'utf8')

class stressTest(object):
    
    
    def __init__(self, url):
        self.press_url = url

    def work(self):
        global ERROR_NUM
        req = request.Request(self.press_url, headers = headers, data = data)
        res = request.urlopen(req)
        print(res.read().decode('utf8'))

    def testonework(self):
        i = 0
        while i < ONE_WORKER_NUM:
            i += 1
            self.work()
        time.sleep(LOOP_SLEEP)

    def run(self):
    # use multithread to do the stress test
        t1 = time.time()
        Threads = []

        for i in range(THREAD_NUM):
            t = threading.Thread(target=self.testonework, name = "T" + str(i))
            t.setDaemon(True)
            Threads.append(t)

        for t in Threads:
            t.start()
        for t in Threads:
            t.join()
        t2 = time.time()

        print("================stress test result===============")
        print("URL: ", self.press_url)
        print("workNum: ", THREAD_NUM, "*", ONE_WORKER_NUM, "=", THREAD_NUM * ONE_WORKER_NUM)
        print("total time cost: ", t2 - t1)
        print("each request cost(s): ", (t2 - t1) / (THREAD_NUM * ONE_WORKER_NUM))
        print("request num/s: ", 1 / ((t2 - t1) / (THREAD_NUM * ONE_WORKER_NUM)))
        print("error num:", ERROR_NUM)


    


if __name__ == '__main__':
    test_url = 'https://us-central1-alpine-province-325707.cloudfunctions.net/ridge'

    THREAD_NUM = 500 # the num of pthreads
    ONE_WORKER_NUM = 10 #the loop times of each pthread
    LOOP_SLEEP = 0.1 #the gap between two request(s)
    ERROR_NUM = 0 #the num of error

    obj = stressTest(test_url)
    obj.run()

