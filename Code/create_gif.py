import sys
from moviepy.editor import *
import os
import time

if not sys.argv[1]:
    print("Please provide a filename. Ex: python3 create_gif.py myMovie.mp4")
    exit()

filename = sys.argv[1].split("/")[-1]
filepath = "/".join(sys.argv[1].split("/")[:len(sys.argv[1].split("/"))-1])

os.system("python -m retro.scripts.playback_movie %s" % filepath + "/" + filename)

clip = VideoFileClip(filepath + "/" + ".".join(filename.split(".")[:len(filename.split("."))-1]) + ".mp4")

clip = clip.subclip()
clip.write_gif("../output/gifs/%s.gif" % filename.split("/")[-1])
os.remove(filepath + "/" + ".".join(filename.split(".")[:len(filename.split("."))-1]) + ".mp4")

