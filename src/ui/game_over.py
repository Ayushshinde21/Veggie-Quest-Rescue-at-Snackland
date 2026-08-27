import pygame


class GameOver:

    def __init__(self, screen):

        self.screen = screen

        self.width = screen.get_width()
        self.height = screen.get_height()

        # ==========================================
        # FONTS
        # ==========================================

        self.title_font = pygame.font.Font(
            None,
            64
        )

        self.option_font = pygame.font.Font(
            None,
            34
        )

        self.info_font = pygame.font.Font(
            None,
            22
        )

        # ==========================================
        # OPTIONS
        # ==========================================

        self.options = [
            "RETRY",
            "MAIN MENU"
        ]

        self.selected = 0

        # ==========================================
        # COLORS
        # ==========================================

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

        self.overlay_color = (
            0,
            0,
            0
        )

    # ==============================================
    # INPUT
    # ==============================================

    def handle_event(self, event):

        if event.type != pygame.KEYDOWN:

            return None

        # ------------------------------------------
        # UP
        # ------------------------------------------

        if event.key in (
            pygame.K_UP,
            pygame.K_w
        ):

            self.selected -= 1

            if self.selected < 0:

                self.selected = (
                    len(self.options) - 1
                )

        # ------------------------------------------
        # DOWN
        # ------------------------------------------

        elif event.key in (
            pygame.K_DOWN,
            pygame.K_s
        ):

            self.selected += 1

            if self.selected >= len(self.options):

                self.selected = 0

        # ------------------------------------------
        # SPACE
        # ------------------------------------------

        elif event.key == pygame.K_SPACE:

            return self.options[
                self.selected
            ]

        # ------------------------------------------
        # ESC
        # ------------------------------------------

        elif event.key == pygame.K_ESCAPE:

            return "MAIN MENU"

        return None

    # ==============================================
    # DRAW
    # ==============================================

    def draw(self):

        # ------------------------------------------
        # DARK OVERLAY
        # ------------------------------------------

        overlay = pygame.Surface(
            (
                self.width,
                self.height
            )
        )

        overlay.set_alpha(180)

        overlay.fill(
            self.overlay_color
        )

        self.screen.blit(
            overlay,
            (0, 0)
        )

        # ------------------------------------------
        # TITLE
        # ------------------------------------------

        title = self.title_font.render(
            "GAME OVER",
            True,
            self.text_color
        )

        title_rect = title.get_rect(
            center=(
                self.width // 2,
                180
            )
        )

        self.screen.blit(
            title,
            title_rect
        )

        # ------------------------------------------
        # OPTIONS
        # ------------------------------------------

        start_y = 320

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
                    start_y + index * 75
                )
            )

            self.screen.blit(
                text,
                text_rect
            )

        # ------------------------------------------
        # INSTRUCTIONS
        # ------------------------------------------

        instruction = self.info_font.render(
            "UP / DOWN  Select     SPACE  Choose",
            True,
            self.text_color
        )

        instruction_rect = instruction.get_rect(
            center=(
                self.width // 2,
                self.height - 60
            )
        )

        self.screen.blit(
            instruction,
            instruction_rect
        )