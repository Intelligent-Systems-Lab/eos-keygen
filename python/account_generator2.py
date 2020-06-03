import sys
import os
from tqdm import tqdm

import argparse
import json

import multiprocessing
from multiprocessing import Pool,Process,Manager
import os, time, random

import subprocess



parser = argparse.ArgumentParser()
parser.add_argument('--user-limit', metavar='', help="Number of users", type=int, default=100)
parser.add_argument('--cores', metavar='', help="Number of cores", type=int, default=2)
parser.add_argument('--save-path', metavar='', help="Path to save keys file", default='./accounts.json')

keys = []


########################################
storage = {
    "producers": [
    ],
    "users": [
    ]
}
# storage['producers'].append({"name":"132", "pvt":"132", "pub":"123"})
########################################


#pbar = tqdm(total=args.user_limit)

def work(i,v,send_end):
    #print("open thread")
    proc = subprocess.Popen('node ../main.js', shell=True,stdout=subprocess.PIPE)
    outs, errs = proc.communicate(timeout=3)
    #l[i] = outs.decode('utf-8').splitlines()
    v.value += 1
    send_end.send(outs.decode('utf-8').splitlines())

    # while True:
    #     try:
    #         proc = subprocess.Popen('node ../main.js', shell=True,stdout=subprocess.PIPE)
    #         #outs = subprocess.check_output('node ../main.js', shell=True, stderr=subprocess.STDOUT,timeout=3)
    #         outs, errs = proc.communicate(timeout=3)
    #         #print(outs.decode('utf-8').splitlines())
    #         #print(outs.decode('utf-8').splitlines())
    #         l[i] = outs.decode('utf-8').splitlines()
    #         v.value += 1
    #     except subprocess.CalledProcessError:
    #         print("time out")
    #         #proc.kill()
    #         #outs, errs = proc.communicate()
            
    #         continue
    #     break
    #print(k)

def screen(v):
    while (int(v.value)<args.user_limit-1):
        print("Process:",int(v.value),"/", args.user_limit)
        time.sleep(2)


#re = result.splitlines()

#print("Result:", keys)

if __name__ == '__main__':
    #keys = Array('i')

    args = parser.parse_args()

    if (args.user_limit<20):
        print("Please set more user.")
        exit()

    manager = Manager()
    v = manager.Value('d', 0.0)
    keys = manager.list(range(args.user_limit))
    pipe_list = []

    pw = Process(target=screen,args=(v,))
    pw.start()
    
    p = Pool(args.cores)
    for i in range(args.user_limit):
        recv_end, send_end = multiprocessing.Pipe(False)
        p.apply_async(work,args=(i,v,send_end))
        #pipe_list.append(recv_end)
        

    p.close()
    p.join() 

    result_list = [x.recv() for x in pipe_list]
    print (result_list)

    pw.join()
    print(keys)
    print("")
    print(len(list(keys)))
    print(type(keys))

    DataFile = open(args.save_path, "w")
    DataFile.write(json.dumps(list(keys), indent=4, sort_keys=True))
    DataFile.close()
