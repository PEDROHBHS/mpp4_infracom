from tkinter import*
import pygame


pygame.mixer.init()


class AudioPlayer:
    def __init__(self, parent : Text, audio_file : str):
        self.parent = parent
        self.audio = audio_file
        self.create_widgets()

    def create_widgets(self):
        global frame
        global play_btn
        global pause_btn
        global stop_btn
        
        frame = Frame(self.parent, width=100, height=40, bg='#000000')
        frame.pack()

        pygame.mixer.music.load(self.audio)

        def pause_handler():
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()

        play_btn = Button(frame, text='Play', command=pygame.mixer.music.play)
        pause_btn = Button(frame, text='Pause', command=pause_handler)
        stop_btn = Button(frame, text='Stop', command=pygame.mixer.music.stop)

        play_btn.pack(side='left')
        pause_btn.pack(side='left')
        stop_btn.pack(side='left')

        self.parent.window_create(END, window=frame)