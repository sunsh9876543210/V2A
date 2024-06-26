import numpy as np


def getAverageL(image):
    """
    Given PIL Image, return average value of grayscale value
    """
    w, h = image.shape[0],image.shape[1]

    return np.average(image.reshape(w * h))
  
def convertnpToAscii(image_array, cols, scale, i):
    lamp = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]
    image = np.transpose(image_array)

    W, H = image.shape[0], image.shape[1]
    w = W / cols
    h = w / scale
    rows = int(H / h)

    if cols > W or rows > H:
        print("Image too small for specified cols!")
        exit(0)
    
    aimg = []

    for j in range(rows):
        y1 = int(j * h)
        y2 = int((j + 1) * h)

        if j == rows - 1:
            y2 = H

        aimg.append("")

        for i in range(cols):
            x1 = int(i * w)
            x2 = int((i + 1) * w)

            if i == cols - 1:
                x2 = W
            
            img = image[x1 : x2, y1 : y2]
            avg = int(getAverageL(img))

            gsval = lamp[int((avg * len(lamp) - 1) / 255)]
            aimg[j] += gsval
    
    return aimg, cols, rows