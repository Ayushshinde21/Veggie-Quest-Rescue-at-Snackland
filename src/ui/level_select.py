import pygame


class LevelSelect:

    def __init__(self, screen):

        self.screen = screen

        self.width = screen.get_width()
        self.height = screen.get_height()

        # ==========================================
        # FONTS
        # ==========================================

        self.title_font = pygame.font.Font(
            None,
            56
        )

        self.level_font = pygame.font.Font(
            None,
            32
        )

        self.info_font = pygame.font.Font(
            None,
            22
        )

        # ==========================================
        # LEVELS
        # ==========================================

        self.levels = [
            {
                "name": "LEVEL 1",
                "unlocked": True
            },
            {
                "name": "LEVEL 2",
                "unlocked": False
            },
            {
                "name": "LEVEL 3",
                "unlocked": False
            }
        ]

        self.selected = 0

        # ==========================================
        # COLORS
        # ==========================================

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

        self.locked_color = (
            150,
            150,
            150
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

                self.selected = (
                    len(self.levels) - 1
                )

        # ------------------------------------------
        # MOVE DOWN
        # ------------------------------------------

        elif event.key in (
            pygame.K_DOWN,
            pygame.K_s
        ):

            self.selected += 1

            if self.selected >= len(self.levels):

                self.selected = 0

        # ------------------------------------------
        # SELECT WITH SPACE
        # ------------------------------------------

        elif event.key == pygame.K_SPACE:

            selected_level = self.levels[
                self.selected
            ]

            if selected_level["unlocked"]:

                return self.selected + 1

        # ------------------------------------------
        # BACK TO MENU
        # ------------------------------------------

        elif event.key == pygame.K_ESCAPE:

            return "BACK"

        return None

    # ==============================================
    # DRAW
    # ==============================================

    def draw(self):

        self.screen.fill(
            self.background_color
        )

        # ==========================================
        # TITLE
        # ==========================================

        title = self.title_font.render(
            "SELECT LEVEL",
            True,
            self.text_color
        )

        title_rect = title.get_rect(
            center=(
                self.width // 2,
                150
            )
        )

        self.screen.blit(
            title,
            title_rect
        )

        # ==========================================
        # LEVEL OPTIONS
        # ==========================================

        start_y = 300

        for index, level in enumerate(
            self.levels
        ):

            # --------------------------------------
            # COLOR
            # --------------------------------------

            if not level["unlocked"]:

                color = self.locked_color

            elif index == self.selected:

                color = self.selected_color

            else:

                color = self.text_color

            # --------------------------------------
            # LEVEL TEXT
            # --------------------------------------

            text = self.level_font.render(
                level["name"],
                True,
                color
            )

            text_rect = text.get_rect(
                center=(
                    self.width // 2,
                    start_y + index * 70
                )
            )

            self.screen.blit(
                text,
                text_rect
            )

            # --------------------------------------
            # LOCKED TEXT
            # --------------------------------------

            if not level["unlocked"]:

                locked = self.info_font.render(
                    "LOCKED",
                    True,
                    self.locked_color
                )

                locked_rect = locked.get_rect(
                    center=(
                        self.width // 2,
                        start_y + index * 70 + 28
                    )
                )

                self.screen.blit(
                    locked,
                    locked_rect
                )

        # ==========================================
        # INSTRUCTIONS
        # ==========================================

        instruction = self.info_font.render(
            "UP / DOWN  Select     SPACE  Play     ESC  Back",
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

        pygame.display.flip()