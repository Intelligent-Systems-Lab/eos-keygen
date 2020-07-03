from multiprocessing import Process, Pool
import os, time
import random
import time
import subprocess
import argparse
import json
from tqdm import tqdm

symbols = '12345abcdefghijklmnopqrstuvwxyz'

########################################
storage = {
    "producers": [
    ],
    "users": [
    ]
}

storage_txt = []
# storage['producers'].append({"name":"132", "pvt":"132", "pub":"123"})
########################################

parser = argparse.ArgumentParser()
parser.add_argument('--user-limit', metavar='', help="Number of users", type=int, default=100)
parser.add_argument('--numproc', metavar='', help="Number of cores", type=int, default=2)
parser.add_argument('--save-path', metavar='', help="Path to save keys file", default='./accounts.json')


def work(i):
    proc = subprocess.Popen('node ../main.js', shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errs = proc.communicate(timeout=3)
    return outs.decode('utf-8').splitlines()


def show(get_result):
    # for i in get_result:
    #     print(i)
    pass



if __name__ == '__main__':

    args = parser.parse_args()

    if (args.user_limit<20):
        print("Please set more user.")
        exit()

    pool = Pool(args.numproc)

    pbar = tqdm(total=args.user_limit)
    pb_pre = args.user_limit

    #results = pool.map_async(work, [i for i in range(20)], callback=show)
    results = pool.map_async(work, [i for i in range(args.user_limit)], chunksize=1)
    while (True):
        if (results.ready()): break
        remain = results._number_left
        pbar.update(pb_pre-remain)
        pb_pre = remain
        
        time.sleep(0.5)
    pool.close()
    pool.join()

    pbar.close()

    print("Generate task done.")

    results_list = results.get()

    for i in range(len(results_list)):
        name = "user"
        while(len(name)<12):
            name += symbols[random.randint(0,len(symbols)-1)]

        if (i<30):
            storage['producers'].append({"name":name, "pvt":results_list[i][0], "pub":results_list[i][1]})
        else:
            storage['users'].append({"name":name, "pvt":results_list[i][0], "pub":results_list[i][1]})

        storage_txt.append("user"+str('{0:04}'.format(i))+"_name="+name+'\n')
        storage_txt.append("user"+str('{0:04}'.format(i))+"_pvt="+results_list[i][0]+'\n')
        storage_txt.append("user"+str('{0:04}'.format(i))+"_pub="+results_list[i][1]+'\n')

    DataFile = open(args.save_path, "w")
    DataFile.write(json.dumps(storage, indent=4, sort_keys=True))
    DataFile.close()

    fp = open(args.save_path.replace(".json",".txt"), "a")
    fp.writelines(storage_txt)
    fp.close()

    print("Save done.")