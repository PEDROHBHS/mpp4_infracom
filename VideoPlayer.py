from tkinter import*
from tkVideoPlayer import TkinterVideo
from moviepy.editor import *
import multiprocessing
from playsound import playsound
import os
import threading

class VideoPlayer:
    def __init__(self, parent : Text, video_file : str):
        self.parent = parent
        self.video = video_file
        self.create_widgets()

    def create_widgets(self):
        global frame
        global video
        global play_btn
        global pause_btn
        global restart_btn
        
        frame = Frame(self.parent, width=200, height=200, bg='#000000')
        frame.pack_propagate(False)
        frame.pack()
        video_mp3 = VideoFileClip(self.video)
        base, ext = os.path.splitext(self.video)
        video_mp3.audio.write_audiofile(f'{base}.mp3')

        p = multiprocessing.Process(target=playsound, args=(f'{base}.mp3',))
        threading.Thread(target=p.start).start()        

        video = TkinterVideo(frame, scaled=True)
        video.load(r"{}".format(self.video))
        
        def stop_video():
            video.pause()
            video.seek(0)
            p.terminate()
        
        stop_btn = Button(frame, text='Stop', command=stop_video)
        
        video.pack(expand=True, fill='both')
        stop_btn.pack(side='left')

        video.play()

        self.parent.window_create(END, window=frame)