from tkinter import*
from tkVideoPlayer import TkinterVideo


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

        video = TkinterVideo(frame, scaled=True)
        video.load(r"{}".format(self.video))

        play_btn = Button(frame, text='Play', command=video.play)
        pause_btn = Button(frame, text='Pause', command=video.pause)

        def reset_video():
            video.play()
            video.seek(0)

        restart_btn = Button(frame, text='Restart', command=reset_video)

        video.pack(expand=True, fill='both')
        play_btn.pack(side='left')
        pause_btn.pack(side='left')
        restart_btn.pack(side='right')

        video.play()

        self.parent.window_create(END, window=frame)