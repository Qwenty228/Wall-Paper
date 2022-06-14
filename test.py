import imageio as iio
import os
import numpy as np

path = 'data\Karuizawa Kei Winter Blanc-1.m4v'

vid = iio.get_reader(path, format="FFMPEG")

frames = []
_, tail = os.path.split(path)


def get_frame():
    while True:
        for frame in vid:
            yield np.rot90(frame)[::-1]






#writer = iio.get_writer(f"{tail}", fps=12)

