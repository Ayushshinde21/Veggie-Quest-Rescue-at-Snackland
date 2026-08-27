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
from src.ui.level_select import LevelSelect
from src.ui.pause_menu import PauseMenu
from src.ui.game_over import GameOver

from src.systems.save_system import (
    save_game,
    load_game
)

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
        self.level_selected = False
        self.paused = False
        self.game_over = False
        self.victory_screen = False

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

        self.level_select = LevelSelect(
            self.screen
        )

        self.pause_menu = PauseMenu(
            self.screen
        )

        self.game_over_menu = GameOver(
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

            # ======================================
            # WINDOW CLOSE
            # ======================================

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

                if result == "PLAY":

                    load_game(
                        self.level
                    )

                    self.game_started = True

                elif result == "QUIT":

                    self.running = False

                continue

            # ======================================
            # LEVEL SELECT
            # ======================================

            if not self.level_selected:

                result = self.level_select.handle_event(
                    event
                )

                if result == 1:

                    self.level_selected = True

                elif result == "BACK":

                    self.game_started = False

                continue

            # ======================================
            # GAME OVER
            # ======================================

            if self.game_over:

                result = self.game_over_menu.handle_event(
                    event
                )

                # ----------------------------------
                # RETRY
                # ----------------------------------

                if result == "RETRY":

                    self.restart_level()

                # ----------------------------------
                # MAIN MENU
                # ----------------------------------

                elif result == "MAIN MENU":

                    self.game_over = False
                    self.level_selected = False
                    self.game_started = False

                continue

            # ======================================
            # VICTORY SCREEN
            # ======================================

            if self.victory_screen:

                if event.type == pygame.KEYDOWN:

                    # ----------------------------------
                    # PLAY AGAIN
                    # ----------------------------------

                    if event.key == pygame.K_SPACE:

                        self.restart_level()

                        self.victory_screen = False

                        self.game_started = True
                        self.level_selected = True

                    # ----------------------------------
                    # QUIT
                    # ----------------------------------

                    elif event.key == pygame.K_ESCAPE:

                        self.running = False

                continue

            # ======================================
            # PAUSE
            # ======================================

            if self.paused:

                result = self.pause_menu.handle_event(
                    event
                )

                if result == "RESUME":

                    self.paused = False

                elif result == "MAIN MENU":

                    self.paused = False
                    self.level_selected = False
                    self.game_started = False

                continue

            # ======================================
            # GAME EVENTS
            # ======================================

            if event.type == pygame.KEYDOWN:

                # ----------------------------------
                # PAUSE
                # ----------------------------------

                if event.key == pygame.K_ESCAPE:

                    self.paused = True

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
        # MAIN MENU
        # ------------------------------------------

        if not self.game_started:

            return

        # ------------------------------------------
        # LEVEL SELECT
        # ------------------------------------------

        if not self.level_selected:

            return

        # ------------------------------------------
        # GAME OVER
        # ------------------------------------------

        if self.game_over:

            return

        # ------------------------------------------
        # VICTORY SCREEN
        # ------------------------------------------

        if self.victory_screen:

            return

        # ------------------------------------------
        # PAUSED
        # ------------------------------------------

        if self.paused:

            return

        # ------------------------------------------
        # GAME
        # ------------------------------------------

        self.level.update()

        save_game(
            self.level
        )

        # ------------------------------------------
        # CHECK GAME OVER
        # ------------------------------------------

        if self.level.player.health <= 0:

            self.game_over = True

            return

        # ------------------------------------------
        # CHECK VICTORY
        # ------------------------------------------

        if self.level.level_complete:

            self.victory_screen = True

    # ==================================================
    # DRAW
    # ==================================================

    def draw(self):

        # ==========================================
        # MAIN MENU
        # ==========================================

        if not self.game_started:

            self.menu.draw()

            pygame.display.flip()

            return

        # ==========================================
        # LEVEL SELECT
        # ==========================================

        if not self.level_selected:

            self.level_select.draw()

            pygame.display.flip()

            return

        # ==========================================
        # VICTORY SCREEN
        # ==========================================

        if self.victory_screen:

            self.draw_victory_screen()

            return

        # ==========================================
        # NORMAL GAME
        # ==========================================

        self.screen.fill(
            SKY_BLUE
        )

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
        # PAUSE
        # ==========================================

        if self.paused:

            self.pause_menu.draw()

        # ==========================================
        # GAME OVER
        # ==========================================

        if self.game_over:

            self.game_over_menu.draw()

        pygame.display.flip()

    # ==================================================
    # VICTORY SCREEN
    # ==================================================

    def draw_victory_screen(self):

        self.screen.fill(
            SKY_BLUE
        )

        # ==========================================
        # TITLE
        # ==========================================

        title_font = pygame.font.Font(
            None,
            72
        )

        title = title_font.render(
            "LEVEL COMPLETE!",
            True,
            BLACK
        )

        title_rect = title.get_rect(
            center=(
                WIDTH // 2,
                160
            )
        )

        self.screen.blit(
            title,
            title_rect
        )

        # ==========================================
        # SCORE
        # ==========================================

        score_font = pygame.font.Font(
            None,
            40
        )

        score = score_font.render(
            f"Score: {self.level.score}",
            True,
            BLACK
        )

        score_rect = score.get_rect(
            center=(
                WIDTH // 2,
                260
            )
        )

        self.screen.blit(
            score,
            score_rect
        )

        # ==========================================
        # PLAY AGAIN
        # ==========================================

        continue_text = score_font.render(
            "PRESS SPACE TO PLAY AGAIN",
            True,
            BLACK
        )

        continue_rect = continue_text.get_rect(
            center=(
                WIDTH // 2,
                360
            )
        )

        self.screen.blit(
            continue_text,
            continue_rect
        )

        # ==========================================
        # QUIT
        # ==========================================

        quit_text = score_font.render(
            "PRESS ESC TO QUIT",
            True,
            BLACK
        )

        quit_rect = quit_text.get_rect(
            center=(
                WIDTH // 2,
                420
            )
        )

        self.screen.blit(
            quit_text,
            quit_rect
        )

        pygame.display.flip()

    # ==================================================
    # RESTART LEVEL
    # ==================================================

    def restart_level(self):

        self.level = Level()

        self.game_over = False
        self.victory_screen = False
        self.paused = False

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