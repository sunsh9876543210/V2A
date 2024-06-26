import time

import argparse

import tqdm

from pwn import *

parser = argparse.ArgumentParser(
                        prog='Ascii player',
                        description='Player',
                        epilog='By Woojun Sun')


parser.add_argument('-i', '--input', default="./output.txt")
parser.add_argument('-w', '--width', type = int, default = 238)
parser.add_argument('-r', '--rate', type = float, default=24 )
args = parser.parse_args()

try:
  framerate = args.rate
except:
  framerate = 24.0

print(framerate)
array = []

f = open(args.input)
lines = f.readlines()
count = 0
string = ""
for line in tqdm.tqdm(lines):
  string += line
  count += 1
  if(count % 57 == 0):
    array.append(string)
    string = ""
f.close()


r = remote("localhost", 7505)

base_time = time.time()
last_frame = 0
while(True):
  target = int((time.time() - base_time) * framerate)
  if(last_frame != target):
    #print(array[target], flush=True)
    r.sendline(array[target])
    last_frame = target