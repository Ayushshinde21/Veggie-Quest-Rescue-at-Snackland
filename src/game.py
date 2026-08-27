import pygame

from src.settings import (
    WIDTH,
    HEIGHT,
    FPS,
    TITLE,
    SKY_BLUE,
    BLACK
)

from src.world.level import Level
from src.ui.main_menu import MainMenu


class Game:

    def __init__(self):

        # ==========================================
        # PYGAME INITIALIZATION
        # ==========================================

        pygame.init()

        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT)
        )

        pygame.display.set_caption(
            TITLE
        )

        self.clock = pygame.time.Clock()

        # ==========================================
        # GAME STATE
        # ==========================================

        self.running = True

        self.game_started = False

        # ==========================================
        # FONT
        # ==========================================

        self.font = pygame.font.Font(
            None,
            28
        )

        # ==========================================
        # MAIN MENU
        # ==========================================

        self.menu = MainMenu(
            self.screen
        )

        # ==========================================
        # LEVEL
        # ==========================================

        self.level = Level()

    # ==================================================
    # EVENTS
    # ==================================================

    def handle_events(self):

        for event in pygame.event.get():

            # --------------------------------------
            # WINDOW CLOSE
            # --------------------------------------

            if event.type == pygame.QUIT:

                self.running = False

                continue

            # ======================================
            # MAIN MENU
            # ======================================

            if not self.game_started:

                result = self.menu.handle_event(
                    event
                )

                # ----------------------------------
                # PLAY
                # ----------------------------------

                if result == "PLAY":

                    self.game_started = True

                # ----------------------------------
                # QUIT
                # ----------------------------------

                elif result == "QUIT":

                    self.running = False

                continue

            # ======================================
            # GAME EVENTS
            # ======================================

            if event.type == pygame.KEYDOWN:

                # ----------------------------------
                # ESCAPE
                # ----------------------------------

                if event.key == pygame.K_ESCAPE:

                    self.running = False

                # ----------------------------------
                # JUMP
                # ----------------------------------

                elif event.key == pygame.K_SPACE:

                    self.level.player.jump()

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):

        # ------------------------------------------
        # Don't update level while menu is open
        # ------------------------------------------

        if not self.game_started:

            return

        # ------------------------------------------
        # UPDATE LEVEL
        # ------------------------------------------

        self.level.update()

    # ==================================================
    # DRAW
    # ==================================================

    def draw(self):

        # ==========================================
        # MAIN MENU
        # ==========================================

        if not self.game_started:

            self.menu.draw()

            return

        # ==========================================
        # GAME BACKGROUND
        # ==========================================

        self.screen.fill(
            SKY_BLUE
        )

        # ==========================================
        # LEVEL
        # ==========================================

        self.level.draw(
            self.screen
        )

        # ==========================================
        # FPS
        # ==========================================

        fps = int(
            self.clock.get_fps()
        )

        fps_text = self.font.render(
            f"FPS: {fps}",
            True,
            BLACK
        )

        self.screen.blit(
            fps_text,
            (10, 10)
        )

        # ==========================================
        # DISPLAY
        # ==========================================

        pygame.display.flip()

    # ==================================================
    # GAME LOOP
    # ==================================================

    def run(self):

        while self.running:

            # --------------------------------------
            # EVENTS
            # --------------------------------------

            self.handle_events()

            # --------------------------------------
            # UPDATE
            # --------------------------------------

            self.update()

            # --------------------------------------
            # DRAW
            # --------------------------------------

            self.draw()

            # --------------------------------------
            # FPS LIMIT
            # --------------------------------------

            self.clock.tick(
                FPS
            )

        # ==========================================
        # CLEANUP
        # ==========================================

        pygame.quit()