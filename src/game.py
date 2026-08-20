import pygame

from src.settings import WIDTH, HEIGHT, FPS, TITLE


class Game:

    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Create game window
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        # Set window title
        pygame.display.set_caption(TITLE)

        # Create clock
        self.clock = pygame.time.Clock()

        # Controls whether the game is running
        self.running = True

    def handle_events(self):

        for event in pygame.event.get():

            # Close button
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        # Game logic will go here later
        pass

    def draw(self):
        # Fill screen with background color
        self.screen.fill((135, 206, 235))

        # Update display
        pygame.display.flip()

    def run(self):

        while self.running:

            # 1. Handle keyboard/mouse/window events
            self.handle_events()

            # 2. Update game objects
            self.update()

            # 3. Draw everything
            self.draw()

            # Keep game running at 60 FPS
            self.clock.tick(FPS)

        # Close pygame
        pygame.quit()