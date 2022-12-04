# BD1 LEGO Max7219 controller
# Author: Goran Vuksic

import time
import argparse
import random
import numpy as np

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas

def bd1(n, block_orientation, rotate, inreverse):

    # create matrix device
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial,
                     cascaded=n,
                     block_orientation=block_orientation,
                     rotate=rotate,
                     blocks_arranged_in_reverse_order=inreverse)

    # set initial intensity
    intensity = 16
    device.contrast(intensity)

    # initial pattern
    matrixbd1 = [
    [[1,0,1,0,1,1,0,1],[1,1,0,1,1,1,0,1],[1,1,1,0,0,1,0,1],[0,1,1,0,1,0,1,1]],
    [[0,1,1,0,1,0,1,1],[0,1,1,1,0,1,1,0],[0,1,1,1,1,1,0,1],[1,1,0,1,1,0,1,1]],
    [[1,1,0,1,1,1,0,1],[1,1,0,1,1,1,0,1],[1,1,0,1,1,0,1,1],[1,1,0,1,0,1,1,0]],
    [[1,1,1,0,1,1,1,0],[1,1,1,0,1,0,1,1],[1,0,1,1,0,1,1,1],[1,1,1,0,1,1,0,1]],
    [[1,0,0,1,1,1,0,1],[1,1,0,1,1,0,1,1],[0,1,1,1,1,0,1,1],[1,1,0,1,1,0,1,1]],
    [[0,1,1,0,1,0,1,1],[1,1,1,1,1,0,1,1],[1,1,1,0,1,1,1,0],[1,0,1,1,1,1,1,1]],
    [[1,1,0,1,1,1,0,1],[1,1,1,0,1,1,0,1],[1,0,1,1,0,1,0,1],[1,1,0,1,1,0,1,0]],
    [[1,1,0,1,0,1,1,1],[1,0,1,1,1,1,0,1],[1,1,0,0,1,1,0,1],[0,1,1,0,0,1,1,1]]
    ]

    # main loop
    while True:
        # turn on lights
        with canvas(device) as draw:
            for i in range (4):
                for j in range (8):
                    for k in range (8):
                        if matrixbd1[j][i][k] == 1:
                            draw.point((k,j + 24 - 8*i), fill="white")

        # sleep
        time.sleep(0.2)
        
        # change intensity
        intensity = random.randint(1, 8) * 2
        device.contrast(intensity)
        
        # shift matrix
        for a in range (8):
            for b in range (4):
                if a % 2 == 0:
                    matrixbd1[a][b] = np.roll(matrixbd1[a][b], -1)
                else:
                    matrixbd1[a][b] = np.roll(matrixbd1[a][b], 1)
        for a in range (8):
            if a % 2 == 0:
                templastled = matrixbd1[a][0][7]
            else:
                templastled = matrixbd1[a][3][0]
            if a % 2 == 0:
                for b in range (3):
                    matrixbd1[a][b][7] = matrixbd1[a][b + 1][7]
            else:
                for b in range (3, 0, -1):
                    matrixbd1[a][b][0] = matrixbd1[a][b - 1][0]
            if a % 2 == 0:
                matrixbd1[a][b + 1][7] = templastled
            else:
                matrixbd1[a][0][0] = templastled
        
               
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='bd1_max7219 arguments',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--cascaded', '-n', type=int, default=4, help='Number of cascaded MAX7219 LED matrices')
    parser.add_argument('--block-orientation', type=int, default=0, choices=[0, 90, -90], help='Corrects block orientation when wired vertically')
    parser.add_argument('--rotate', type=int, default=1, choices=[0, 1, 2, 3], help='Rotate display 0=0°, 1=90°, 2=180°, 3=270°')
    parser.add_argument('--reverse-order', type=bool, default=False, help='Set to true if blocks are in reverse order')

    args = parser.parse_args()

    try:
        bd1(args.cascaded, args.block_orientation, args.rotate, args.reverse_order)
    except KeyboardInterrupt:
        pass
