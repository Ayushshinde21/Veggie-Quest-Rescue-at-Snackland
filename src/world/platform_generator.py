import random
import math

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

        # ==========================================
        # DIFFICULTY
        # ==========================================

        self.base_difficulty = 1.5

        # ==========================================
        # PLAYER PHYSICS
        # ==========================================

        self.speed = PLAYER_SPEED
        self.gravity = PLAYER_GRAVITY
        self.jump_strength = abs(
            PLAYER_JUMP_STRENGTH
        )

        self.max_jump_height = (
            self.jump_strength ** 2
            / (2 * self.gravity)
        )

        # ==========================================
        # LANDING TOLERANCE
        # ==========================================

        self.landing_tolerance = 10

    # ==============================================
    # DIFFICULTY
    # ==============================================

    def get_difficulty(self, x):

        progress = x / self.world_width

        progress = max(
            0.0,
            min(1.0, progress)
        )

        return (
            self.base_difficulty
            + progress * 1.5
        )

    # ==============================================
    # LANDING TIME
    # ==============================================

    def get_landing_time(
        self,
        vertical_difference
    ):

        a = 0.5 * self.gravity
        b = -self.jump_strength
        c = -vertical_difference

        discriminant = (
            b * b
            - 4 * a * c
        )

        if discriminant < 0:
            return None

        sqrt_discriminant = math.sqrt(
            discriminant
        )

        time1 = (
            -b + sqrt_discriminant
        ) / (2 * a)

        time2 = (
            -b - sqrt_discriminant
        ) / (2 * a)

        return max(
            time1,
            time2
        )

    # ==============================================
    # REACHABILITY
    # ==============================================

    def can_reach_platform(
        self,
        current_platform,
        next_x,
        next_y,
        next_width
    ):

        vertical_difference = (
            next_y
            - current_platform.rect.y
        )

        # Too high
        if (
            -vertical_difference
            > self.max_jump_height
        ):
            return False

        landing_time = self.get_landing_time(
            vertical_difference
        )

        if landing_time is None:
            return False

        reachable_distance = (
            self.speed
            * landing_time
        )

        actual_gap = (
            next_x
            - current_platform.rect.right
        )

        reachable_distance += (
            self.landing_tolerance
        )

        return (
            actual_gap
            <= reachable_distance
        )

    # ==============================================
    # PLATFORM SIZE
    # ==============================================

    def get_platform_settings(
        self,
        difficulty
    ):

        min_width = int(
            100 - difficulty * 15
        )

        max_width = int(
            150 - difficulty * 25
        )

        min_width = max(
            60,
            min_width
        )

        max_width = max(
            min_width + 10,
            max_width
        )

        min_gap = int(
            90 + difficulty * 15
        )

        max_gap = int(
            125 + difficulty * 20
        )

        max_height_change = int(
            70 + difficulty * 20
        )

        return (
            min_width,
            max_width,
            min_gap,
            max_gap,
            max_height_change
        )

    # ==============================================
    # CREATE PLATFORM
    # ==============================================

    def try_create_platform(
        self,
        current_platform,
        current_y,
        pattern
    ):

        difficulty = self.get_difficulty(
            current_platform.rect.x
        )

        (
            min_width,
            max_width,
            min_gap,
            max_gap,
            max_height_change
        ) = self.get_platform_settings(
            difficulty
        )

        # ------------------------------------------
        # PATTERN: STAIRCASE
        # ------------------------------------------

        if pattern == "staircase":

            height_change = random.randint(
                40,
                max_height_change
            )

        # ------------------------------------------
        # PATTERN: DESCENDING
        # ------------------------------------------

        elif pattern == "descending":

            height_change = random.randint(
                -max_height_change,
                -40
            )

        # ------------------------------------------
        # PATTERN: ZIG-ZAG
        # ------------------------------------------

        elif pattern == "zigzag":

            height_change = random.choice([
                random.randint(
                    40,
                    max_height_change
                ),
                random.randint(
                    -max_height_change,
                    -40
                )
            ])

        # ------------------------------------------
        # PATTERN: HIGH-LOW
        # ------------------------------------------

        elif pattern == "high_low":

            height_change = random.choice([
                random.randint(
                    50,
                    max_height_change
                ),
                random.randint(
                    -max_height_change,
                    -50
                )
            ])

        # ------------------------------------------
        # PATTERN: NORMAL
        # ------------------------------------------

        else:

            height_change = random.randint(
                -max_height_change,
                max_height_change
            )

        # ------------------------------------------
        # NEW POSITION
        # ------------------------------------------

        gap = random.randint(
            min_gap,
            max_gap
        )

        width = random.randint(
            min_width,
            max_width
        )

        new_x = (
            current_platform.rect.right
            + gap
        )

        new_y = current_y + height_change

        # Keep inside playable area

        new_y = max(
            150,
            min(
                HEIGHT - 150,
                new_y
            )
        )

        # ------------------------------------------
        # REACHABILITY CHECK
        # ------------------------------------------

        if not self.can_reach_platform(
            current_platform,
            new_x,
            new_y,
            width
        ):
            return None

        return Platform(
            new_x,
            new_y,
            width
        )

    # ==============================================
    # GENERATE LEVEL
    # ==============================================

    def generate(self):

        platforms = []

        # ==========================================
        # START PLATFORM
        # ==========================================

        current_x = 100
        current_y = HEIGHT - 160

        first_width = 250

        first_platform = Platform(
            current_x,
            current_y,
            first_width
        )

        platforms.append(
            first_platform
        )

        current_platform = first_platform

        # ==========================================
        # PATTERN LIST
        # ==========================================

        patterns = [
            "normal",
            "staircase",
            "zigzag",
            "high_low",
            "descending"
        ]

        # ==========================================
        # GENERATE
        # ==========================================

        while current_x < (
            self.world_width - 400
        ):

            # Choose a pattern

            pattern = random.choice(
                patterns
            )

            platform_created = False

            # Try several times

            for _ in range(100):

                platform = self.try_create_platform(
                    current_platform,
                    current_y,
                    pattern
                )

                if platform is None:
                    continue

                # Add platform

                platforms.append(
                    platform
                )

                # Update current platform

                current_platform = platform

                current_x = platform.rect.x
                current_y = platform.rect.y

                platform_created = True

                break

            # --------------------------------------
            # SAFETY
            # --------------------------------------

            if not platform_created:
                break

        return platforms