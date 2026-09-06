import pygame


class MainMenu:

    def __init__(self, screen):

        self.screen = screen

        self.width = screen.get_width()
        self.height = screen.get_height()

        # ------------------------------------------
        # FONT
        # ------------------------------------------

        self.title_font = pygame.font.Font(
            None,
            64
        )

        self.option_font = pygame.font.Font(
            None,
            36
        )

        # ------------------------------------------
        # OPTIONS
        # ------------------------------------------

        self.options = [
            "PLAY",
            "QUIT"
        ]

        self.selected = 0

        # ------------------------------------------
        # COLORS
        # ------------------------------------------

        self.background_color = (
            80,
            180,
            220
        )

        self.text_color = (
            255,
            255,
            255
        )

        self.selected_color = (
            255,
            220,
            80
        )

    # ==============================================
    # UNLOCK LEVEL
    # ==============================================

    def unlock_level(self, level_number):

        if level_number < 1:
            return

        if level_number > len(self.levels):
            return

        self.levels[level_number - 1]["unlocked"] = True

    # ==============================================
    # INPUT
    # ==============================================

    def handle_event(self, event):

        if event.type != pygame.KEYDOWN:
            return None

        # ------------------------------------------
        # MOVE UP
        # ------------------------------------------

        if event.key in (
            pygame.K_UP,
            pygame.K_w
        ):

            self.selected -= 1

            if self.selected < 0:
                self.selected = len(self.options) - 1

        # ------------------------------------------
        # MOVE DOWN
        # ------------------------------------------

        elif event.key in (
            pygame.K_DOWN,
            pygame.K_s
        ):

            self.selected += 1

            if self.selected >= len(self.options):
                self.selected = 0

        # ------------------------------------------
        # SELECT
        # ------------------------------------------

        elif event.key in (
            pygame.K_RETURN,
            pygame.K_SPACE
        ):

            return self.options[self.selected]

        # ------------------------------------------
        # QUIT
        # ------------------------------------------

        elif event.key == pygame.K_ESCAPE:

            return "QUIT"

        return None

    # ==============================================
    # DRAW
    # ==============================================

    def draw(self):

        self.screen.fill(
            self.background_color
        )

        # ------------------------------------------
        # TITLE
        # ------------------------------------------

        title = self.title_font.render(
            "VEGGIE QUEST",
            True,
            self.text_color
        )

        title_rect = title.get_rect(
            center=(
                self.width // 2,
                self.height // 3
            )
        )

        self.screen.blit(
            title,
            title_rect
        )

        # ------------------------------------------
        # OPTIONS
        # ------------------------------------------

        start_y = (
            self.height // 2
        )

        for index, option in enumerate(
            self.options
        ):

            if index == self.selected:

                color = self.selected_color

            else:

                color = self.text_color

            text = self.option_font.render(
                option,
                True,
                color
            )

            text_rect = text.get_rect(
                center=(
                    self.width // 2,
                    start_y + index * 60
                )
            )

            self.screen.blit(
                text,
                text_rect
            )

        pygame.display.flip()