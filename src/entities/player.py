import pygame

from src.entities.game_object import GameObject


class Player(GameObject):

    def __init__(self, x, y):

        # Player size
        super().__init__(x, y, 40, 60)

        # Movement
        self.speed = 5

        # Vertical movement
        self.velocity_y = 0

        # Physics
        self.gravity = 0.8

        # Jump
        self.jump_strength = -15

        # State
        self.on_ground = False

        # Health
        self.health = 3

    def handle_input(self):

        keys = pygame.key.get_pressed()

        # Horizontal movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed

    def jump(self):

        if self.on_ground:
            self.velocity_y = self.jump_strength
            self.on_ground = False

    def apply_gravity(self):

        self.velocity_y += self.gravity

        self.rect.y += self.velocity_y

    def update(self, platforms):

        # Store previous position
        previous_rect = self.rect.copy()

        # Horizontal movement
        self.handle_input()

        # Keep player inside screen
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > 960:
            self.rect.right = 960

        # Apply gravity
        self.apply_gravity()

        self.on_ground = False

        # Check collisions
        for platform in platforms:

            if self.rect.colliderect(platform.rect):

                # Falling onto platform
                if (
                        self.velocity_y >= 0
                        and previous_rect.bottom <= platform.rect.top
                ):
                    self.rect.bottom = platform.rect.top

                    self.velocity_y = 0

                    self.on_ground = True

    def draw(self, screen):

        # Temporary carrot representation
        pygame.draw.rect(
            screen,
            (255, 140, 0),
            self.rect
        )

        # Green carrot leaves
        pygame.draw.rect(
            screen,
            (50, 180, 70),
            (
                self.rect.x + 10,
                self.rect.y - 10,
                20,
                12
            )
        )