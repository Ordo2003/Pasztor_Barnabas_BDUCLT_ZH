import pygame
import os


class PB_MetroMusic:
    def __init__(self, music_path):
        self.music_path = music_path
        self.playing = False
        self.paused = False
        pygame.mixer.init()

    def play_music(self):
        if not os.path.exists(self.music_path):
            return
        try:
            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.play(loops=-1)
            self.playing = True
            self.paused = False
        except Exception:
            pass

    def toggle_music(self):
        if not self.playing:
            self.play_music()
            return
        if not self.paused:
            pygame.mixer.music.pause()
            self.paused = True
        else:
            pygame.mixer.music.unpause()
            self.paused = False

    def stop_music(self):
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except Exception:
            pass