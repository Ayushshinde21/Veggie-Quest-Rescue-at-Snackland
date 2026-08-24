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

        # Maximum theoretical jump height
        self.max_jump_height = (
            self.jump_strength ** 2
            / (2 * self.gravity)
        )

        # ==========================================
        # LANDING TOLERANCE
        # ==========================================

        self.landing_tolerance = 15

        # ==========================================
        # JUMP LIMITS
        # ==========================================

        # Don't use the absolute maximum.
        # Keep some safety margin.

        self.safe_jump_height = (
            self.max_jump_height * 0.85
        )

        self.max_jump_distance = 220

        self.min_horizontal_gap = 35

        # ==========================================
        # PLATFORM SETTINGS
        # ==========================================

        self.minimum_platform_width = 60

    # ==============================================
    # DIFFICULTY
    # ==============================================

    def get_difficulty(self, x):

        progress = (
            x / self.world_width
        )

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

        # Equation:
        #
        # y = v*t + 1/2*g*t²
        #
        # We want the positive landing time.

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

        # We need the positive solution
        # corresponding to the landing.

        valid_times = [
            t
            for t in (time1, time2)
            if t > 0
        ]

        if not valid_times:

            return None

        return max(valid_times)

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

        current_top = (
            current_platform.rect.top
        )

        # ------------------------------------------
        # VERTICAL DIFFERENCE
        # ------------------------------------------

        vertical_difference = (
            next_y
            - current_top
        )

        # ------------------------------------------
        # PLATFORM TOO HIGH
        # ------------------------------------------

        if (
            -vertical_difference
            > self.safe_jump_height
        ):

            return False

        # ------------------------------------------
        # PLATFORM TOO LOW
        # ------------------------------------------

        # Very large drops are avoided because
        # they make the next landing unreliable.

        if vertical_difference > 120:

            return False

        # ------------------------------------------
        # LANDING TIME
        # ------------------------------------------

        landing_time = (
            self.get_landing_time(
                vertical_difference
            )
        )

        if landing_time is None:

            return False

        # ------------------------------------------
        # HORIZONTAL DISTANCE PLAYER CAN TRAVEL
        # ------------------------------------------

        reachable_distance = (
            self.speed
            * landing_time
        )

        # Add player's landing tolerance.

        reachable_distance += (
            self.landing_tolerance
        )

        # ------------------------------------------
        # ACTUAL GAP
        # ------------------------------------------

        current_right = (
            current_platform.rect.right
        )

        actual_gap = (
            next_x
            - current_right
        )

        # ------------------------------------------
        # TOO FAR
        # ------------------------------------------

        if (
            actual_gap
            > self.max_jump_distance
        ):

            return False

        if (
            actual_gap
            > reachable_distance
        ):

            return False

        # ------------------------------------------
        # NEGATIVE GAP
        # ------------------------------------------

        # Don't allow platforms to overlap in
        # the normal generated sequence.

        if actual_gap < self.min_horizontal_gap:

            return False

        return True

    # ==============================================
    # PLATFORM SIZE
    # ==============================================

    def get_platform_settings(
        self,
        difficulty
    ):

        min_width = int(
            130 - difficulty * 10
        )

        max_width = int(
            190 - difficulty * 15
        )

        min_width = max(
            self.minimum_platform_width,
            min_width
        )

        max_width = max(
            min_width + 10,
            max_width
        )

        # ------------------------------------------
        # GAP
        # ------------------------------------------

        min_gap = int(
            100 + difficulty * 14
        )

        max_gap = int(
            140 + difficulty * 18
        )

        # Don't generate gaps beyond our
        # maximum safe distance.

        max_gap = min(
            max_gap,
            self.max_jump_distance
        )

        # ------------------------------------------
        # HEIGHT CHANGE
        # ------------------------------------------

        max_height_change = int(
            70 + difficulty * 20
        )

        # Keep height change within safe jump range.

        max_height_change = min(
            max_height_change,
            int(self.safe_jump_height)
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

        # ==========================================
        # HEIGHT PATTERN
        # ==========================================

        if pattern == "staircase":

            height_change = random.randint(
                40,
                max_height_change
            )

        elif pattern == "descending":

            height_change = random.randint(
                -max_height_change,
                -40
            )

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

        else:

            height_change = random.randint(
                -max_height_change,
                max_height_change
            )

        # ==========================================
        # GAP
        # ==========================================

        gap = random.randint(
            min_gap,
            max_gap
        )

        # ==========================================
        # WIDTH
        # ==========================================

        width = random.randint(
            min_width,
            max_width
        )

        # ==========================================
        # POSITION
        # ==========================================

        new_x = (
            current_platform.rect.right
            + gap
        )

        new_y = (
            current_y
            + height_change
        )

        # ==========================================
        # WORLD BOUNDARY
        # ==========================================

        new_y = max(
            150,
            min(
                HEIGHT - 150,
                new_y
            )
        )

        # ==========================================
        # REACHABILITY
        # ==========================================

        if not self.can_reach_platform(
            current_platform,
            new_x,
            new_y,
            width
        ):

            return None

        # ==========================================
        # CREATE PLATFORM
        # ==========================================

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

        current_y = (
            HEIGHT - 160
        )

        first_width = 250

        first_platform = Platform(
            current_x,
            current_y,
            first_width
        )

        platforms.append(
            first_platform
        )

        current_platform = (
            first_platform
        )

        # ==========================================
        # PATTERNS
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

            pattern = random.choice(
                patterns
            )

            platform_created = False

            # ======================================
            # RETRY
            # ======================================

            for _ in range(100):

                platform = (
                    self.try_create_platform(
                        current_platform,
                        current_y,
                        pattern
                    )
                )

                if platform is None:

                    continue

                # ==================================
                # ADD PLATFORM
                # ==================================

                platforms.append(
                    platform
                )

                # ==================================
                # UPDATE
                # ==================================

                current_platform = platform

                current_x = (
                    platform.rect.x
                )

                current_y = (
                    platform.rect.y
                )

                platform_created = True

                break

            # ======================================
            # SAFETY
            # ======================================

            if not platform_created:

                break

        return platforms