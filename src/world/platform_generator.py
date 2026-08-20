import random

from src.entities.platform import Platform
from src.settings import (
    HEIGHT,
    PLAYER_SPEED,
    PLAYER_GRAVITY,
    PLAYER_JUMP_STRENGTH
)


class PlatformGenerator:

    def __init__(self, world_width):

        self.world_width = world_width

        # -----------------------------------------
        # DIFFICULTY
        # -----------------------------------------

        # Higher = harder
        self.difficulty = 1.5

        # -----------------------------------------
        # JUMP CALCULATION
        # -----------------------------------------

        # Approximate total time in air
        self.jump_time = (
            2 * abs(PLAYER_JUMP_STRENGTH)
            / PLAYER_GRAVITY
        )

        # Approximate maximum horizontal travel
        self.max_jump_distance = (
            PLAYER_SPEED * self.jump_time
        )

        # -----------------------------------------
        # PLATFORM SETTINGS
        # -----------------------------------------

        # Empty space between platforms
        self.min_gap = 110
        self.max_gap = 160

        # Smaller platforms = harder landing
        self.min_width = 70
        self.max_width = 105

        # Vertical variation
        self.max_height_change = 110

    # ---------------------------------------------
    # GENERATE LEVEL
    # ---------------------------------------------

    def generate(self):

        platforms = []

        # -----------------------------------------
        # STARTING PLATFORM
        # -----------------------------------------

        current_x = 100
        current_y = HEIGHT - 160

        previous_width = 250

        first_platform = Platform(
            current_x,
            current_y,
            previous_width
        )

        platforms.append(
            first_platform
        )

        # -----------------------------------------
        # GENERATE RANDOM PLATFORMS
        # -----------------------------------------

        while current_x < self.world_width - 400:

            # Random gap between platform edges
            gap = random.randint(
                self.min_gap,
                self.max_gap
            )

            # Random platform width
            width = random.randint(
                self.min_width,
                self.max_width
            )

            # Random vertical difference
            height_change = random.randint(
                -self.max_height_change,
                self.max_height_change
            )

            new_y = current_y + height_change

            # Keep platform inside playable area
            new_y = max(
                150,
                min(
                    HEIGHT - 150,
                    new_y
                )
            )

            # Move after previous platform
            current_x += previous_width + gap

            # Create platform
            platform = Platform(
                current_x,
                new_y,
                width
            )

            platforms.append(
                platform
            )

            # Save current platform information
            current_y = new_y
            previous_width = width

        return platforms