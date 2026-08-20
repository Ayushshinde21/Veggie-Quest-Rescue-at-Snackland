import pygame

from src.settings import (
    WIDTH,
    HEIGHT,
    FPS,
    TITLE,
    SKY_BLUE,
    GROUND_GREEN,
    WHITE,
    BLACK
)

from src.entities.game_object import GameObject
from src.entities.player import Player

class Game:

    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        pygame.display.set_caption(TITLE)

        self.clock = pygame.time.Clock()

        self.running = True

        # Font for FPS
        self.font = pygame.font.Font(None, 28)

        # Create ground
        self.ground = GameObject(
            0,
            HEIGHT - 80,
            WIDTH,
            80
        )

        # Create player
        self.player = Player(
            100,
            HEIGHT - 200
        )

    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.running = False

                if event.key == pygame.K_SPACE:
                    self.player.jump()

    def update(self):

        self.ground.update()
        self.player.update(self.ground)

    def draw(self):

        # Background
        self.screen.fill(SKY_BLUE)

        # Draw ground
        pygame.draw.rect(
            self.screen,
            GROUND_GREEN,
            self.ground.rect
        )
        # Draw player
        self.player.draw(self.screen)

        # FPS
        fps = int(self.clock.get_fps())

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

    def run(self):

        while self.running:

            self.handle_events()

            self.update()

            self.draw()

            self.clock.tick(FPS)

        pygame.quit()