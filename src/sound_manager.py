import pygame
import os


class SoundManager:

    def __init__(self):

        self.sounds = {}

        sound_folder = os.path.join(
            "assets",
            "sounds"
        )

        sound_files = {
            "jump": "jump.wav",
            "collect": "collect.wav",
            "checkpoint": "checkpoint.wav",
            "damage": "damage.wav",
            "stomp": "stomp.wav",
            "death": "death.wav"
        }

        for name, filename in sound_files.items():

            path = os.path.join(
                sound_folder,
                filename
            )

            if not os.path.exists(path):
                print(
                    f"Sound file not found: {path}"
                )

                continue

            try:

                self.sounds[name] = (
                    pygame.mixer.Sound(path)
                )

                print(
                    f"Loaded sound: {name}"
                )

            except pygame.error as error:

                print(
                    f"Could not load {path}: {error}"
                )

    # ==========================================
    # PLAY SOUND
    # ==========================================

    def play(self, name):

        if name in self.sounds:

            self.sounds[name].play()

    # ==========================================
    # BACKGROUND MUSIC
    # ==========================================

    def play_music(self):
        music_path = os.path.join("assets", "music", "background.mp3")

        print("Looking for music:", music_path)
        print("Music exists:", os.path.exists(music_path))

        if not os.path.exists(music_path):
            print("Music file not found!")
            return

        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1)

            print("Background music started")

        except pygame.error as error:
            print("Could not load music:", error)

    # ==========================================
    # STOP MUSIC
    # ==========================================

    def stop_music(self):

        pygame.mixer.music.stop()