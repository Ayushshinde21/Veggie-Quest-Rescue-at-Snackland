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


class Game:

    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT)
        )

        pygame.display.set_caption(TITLE)

        self.clock = pygame.time.Clock()

        self.running = True

        self.font = pygame.font.Font(
            None,
            28
        )

        # Create level
        self.level = Level()

    # --------------------------------------------------
    # EVENTS
    # --------------------------------------------------

    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                self.running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    self.running = False

                if event.key == pygame.K_SPACE:

                    self.level.player.jump()

    # --------------------------------------------------
    # UPDATE
    # --------------------------------------------------

    def update(self):

        self.level.update()

    # --------------------------------------------------
    # DRAW
    # --------------------------------------------------

    def draw(self):

        # Background
        self.screen.fill(
            SKY_BLUE
        )

        # Draw level
        self.level.draw(
            self.screen
        )

        # FPS
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

        pygame.display.flip()

    # --------------------------------------------------
    # GAME LOOP
    # --------------------------------------------------

    def run(self):

        while self.running:

            self.handle_events()

            self.update()

            self.draw()

            self.clock.tick(FPS)

        pygame.quit()