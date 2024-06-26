import convert_ascii
import getshape
import numpy as np

import cupy as cp

from PIL import Image, ImageFilter
import os

import tqdm

import ffmpeg

import argparse

def convert(path, wd, width, output):
    print(f'ffpb -hwaccel nvdec -i "{path}" "{wd}\\%06d.png"')
    #os.system(f'ffpb -hwaccel nvdec -i "{path}" "{wd}\\%06d.png"')
    #todo

    frame_count = len(os.listdir(wd))

    f = open(output, 'w', encoding='utf-8')
    for i in tqdm.tqdm(range(1, frame_count+1)):
        input = np.array(Image.open(f'{wd}\\%06d.png'%(i)).convert("L"))

        converted, cols, rows = convert_ascii.convertnpToAscii(input, width, 0.43, i)
        if i == 1:
            print(cols, rows)
        string = ""
        for i in converted:
            string += i + "\n"
        f.write(string)
        
        


if __name__ == "__main__" :
    parser = argparse.ArgumentParser(
                        prog='V2A',
                        description='Simple Video to ASCII tool',
                        epilog='By Woojun Sun')

    parser.add_argument('filename')
    parser.add_argument('-o', '--output', default="./output.txt")
    parser.add_argument('-w', '--width', type = int, default = 238)

    args = parser.parse_args()


    file_dir = args.filename
    file_name = args.filename
    file_abspath = args.filename
    width = args.width
    w_dir = ""

    if os.path.isfile(file_dir):
        filename, file_ext = os.path.splitext(file_dir)
        file_name = filename + file_ext # filename without directory
        file_abspath = os.path.abspath(file_dir) #absolute path
        os.makedirs(filename, exist_ok=True)
        w_dir = os.path.abspath(os.path.dirname(file_dir)) + '\\' + filename
        
    else :
        print(f'{file_dir} : File does not exist')
        exit(0)

    convert(file_abspath, w_dir, width, args.output)

    