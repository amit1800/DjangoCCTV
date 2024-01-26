from typing import Any, Coroutine, Union
import numpy as np
import cv2
import os
from aiortc import VideoStreamTrack
from av import VideoFrame
import random
import time
from fractions import Fraction
import asyncio

image = np.zeros((240, 360, 3), dtype=np.uint8)


class CustomVideoTrack(VideoStreamTrack):
    pts = 0

    def isInt(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def __init__(self, framerate) -> None:
        if self.isInt(framerate):
            self.framerate = int(framerate)
        else:
            self.framerate = 1
        super().__init__()

    async def recv(self):
        start_time = time.time()
        # frame =await self.track.recv()
        await asyncio.sleep(1 / self.framerate)
        # print("%s seconds" % (time.time() - start_time))
        image[:, :] = [
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        ]
        nframe = VideoFrame.from_ndarray(image, format="bgr24")
        nframe.pts = self.pts
        self.pts += 90000 / self.framerate
        nframe.time_base = Fraction(1, 90000)
        # print(nframe.pts, nframe.time_base)
        return nframe
