import sys
import os
from tqdm import tqdm
import random
import argparse
import json
#import numpy


#result = os.system('node ../main.js')
#result = os.popen('node ../main.js').read()

symbols = '12345abcdefghijklmnopqrstuvwxyz'

parser = argparse.ArgumentParser()

parser.add_argument('--user-limit', metavar='', help="Number of users", type=int, default=100)
parser.add_argument('--save-path', metavar='', help="Path to save keys file", default='./accounts.json')

args = parser.parse_args()

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

if (args.user_limit<20):
    print("Please set more user.")
    exit()


pbar = tqdm(total=args.user_limit)

for i in range(args.user_limit):
    #if i%2==0: print("Generate : ",i,"/",args.user_limit)
    k = os.popen('node ../main.js').read()
    k = k.splitlines()
    #name = "user"+str('{0:08}'.format(i))
    name = "user"
    while(len(name)<12):
        name += symbols[random.randint(0,len(symbols)-1)]

    if (i<30):
        storage['producers'].append({"name":name, "pvt":k[0], "pub":k[1]})
    else:
        storage['users'].append({"name":name, "pvt":k[0], "pub":k[1]})
    pbar.update()
    
pbar.close()

DataFile = open(args.save_path, "w")
DataFile.write(json.dumps(storage, indent=4, sort_keys=True))
DataFile.close()
#re = result.splitlines()

#print("Result:", keys)
