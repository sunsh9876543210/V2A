import time

import argparse

import unicodedata

import socketserver

import re

parser = argparse.ArgumentParser(
                        prog='Ascii player',
                        description='Player',
                        epilog='By Woojun Sun')


parser.add_argument('-i', '--input', default="./output.txt")
parser.add_argument('-w', '--width', type = int, default = 238)
parser.add_argument('-r', '--rate', type = float, default=24 )
parser.add_argument('-s', '--subtitle', default="")
args = parser.parse_args()

try:
  framerate = args.rate
except:
  framerate = 24.0

subtitle = True if args.subtitle != "" else False

width = args.width
print(framerate)
array = []
subtitles = []

f = open(args.input)
lines = f.readlines()
count = 0
string = b""
for line in lines:
  string += line.encode()
  count += 1
  if(count % 57 == 0):
    array.append(string)
    string = b"\n\n\n\n"
f.close()

if subtitle:
  f = open(args.subtitle)
  lines = f.readlines()
  lines = [line.rstrip('\n') for line in lines]
  if(not "WEBVTT" in lines[0]):
    print("not an webvtt subtitle")
    exit()
  _str = ""
  now = 0
  while now < len(lines):
    if(" --> " in lines[now]):
      s, e = lines[now].split(" --> ")
      sh, sm, ss = map(float, s.split(':'))
      eh, em, es = map(float, e.split(' ')[0].split(':'))
      start = sh * 3600 + sm * 60 + ss
      end = eh * 3600 + em * 60 + es
      while lines[now] != "":
        now += 1
        deleted = re.sub(r'<[^>]*>','',lines[now])
        _str += deleted + '\n'
      subtitles.append((start, end, _str.rstrip('\n')))
      _str = ""
    now += 1
print("Loading done!")

def second2time(sec):
  hour = int(sec / 3600)
  minute = int(sec / 60) - hour * 60
  sec = sec % 60
  return hour, minute, sec

def time2str(sec):
  hour, minute, sec = second2time(sec)
  s_h, s_m, s_s = str(hour).zfill(2), str(minute).zfill(2), str(sec).zfill(2)
  if(hour > 0):
    return f'{s_h}:{s_m}:{s_s}'
  else:
    return f'{s_m}:{s_s}'
  
def pad(string, length):
  lenl = (length - stringWidth(string)) // 2
  lenr = length - stringWidth(string) - lenl
  return ' ' * lenl + string + ' ' * lenr

def stringWidth(string): #Thank you : https://stackoverflow.com/questions/48598304/width-of-a-string-with-zero-width-and-two-width-characters-in-python-3-in-a-ter
    width = 0
    for c in string:
        # For zero-width characters
        if unicodedata.category(c)[0] in ('M', 'C'):
            continue
        w = unicodedata.east_asian_width(c)
        if w in ('N', 'Na', 'H', 'A'):
            width += 1
        else:
            width += 2

    return width

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
  def handle(self):
    print(f"Request from {self.client_address}")
    base_time = time.time()
    last_frame = 0
    target = 0
    array_len = len(array)
    full_time = int(array_len / framerate)
    full_payload = time2str(full_time).encode()

    sub_index = 0
    try:
      self.request.send(b'\033[2J')
      while True:
        now = time.time() - base_time
        target = int((now) * framerate)
        time_r = int(time.time() - base_time)
        payload = time2str(time_r).encode()
        if(sub_index < len(subtitles)):
          nowsub = subtitles[sub_index][2]

          if(subtitles[sub_index][0] > now):
            nowsub = ""

          if(subtitles[sub_index][1] < now):
            sub_index += 1
        else:
            nowsub = ""
        if(last_frame != target):
          if target < array_len:
            to_send = b'\033[H' + array[target]
            sub_height = len(nowsub.split('\n'))
            for i in nowsub.split('\n'):
              to_send += b'\n' + pad(i, width).encode()
            to_send += (b'\n' + b' ' * width) * max(0,(4 - sub_height))
            to_send += b'\n' + payload + b' / ' + full_payload
            to_send += b'\n' + b'=' * int(width * (time.time() - base_time) / full_time)
            self.request.send(to_send)
          else:
            break
        last_frame = target
    except ConnectionResetError as e:
      print(f'exception : {e}')
      pass
    self.request.send(b'\n\n\n\n' + b'-' * 117 + b'EOF!' + b'-' * 117 + b'\n')
    self.request.close()
    print(f"Closed {self.client_address}")
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
  pass

with ThreadedTCPServer(("0.0.0.0",9999), ThreadedTCPRequestHandler) as server:
  server.timeout = None
  server.serve_forever()
