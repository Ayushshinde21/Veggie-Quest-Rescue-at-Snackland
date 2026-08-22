import pygame


class Enemy:

    def __init__(
        self,
        x,
        y,
        left_limit,
        right_limit,
        speed=2,
        enemy_type="slime",
        platform_top=None
    ):

        # ==========================================
        # POSITION
        # ==========================================

        if enemy_type == "heavy":

            width = 50
            height = 50

        else:

            width = 32
            height = 32

        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        # ==========================================
        # MOVEMENT
        # ==========================================

        self.speed = speed

        self.direction = 1

        # ==========================================
        # PATROL LIMITS
        # ==========================================

        self.left_limit = left_limit

        self.right_limit = right_limit

        # ==========================================
        # TYPE
        # ==========================================

        self.enemy_type = enemy_type

        # ==========================================
        # STATE
        # ==========================================

        self.alive = True

        # ==========================================
        # JUMPER
        # ==========================================

        self.velocity_y = 0

        self.gravity = 0.5

        self.jump_strength = -9

        self.jump_timer = 0

        self.jump_delay = 120

        self.platform_top = platform_top

        # ==========================================
        # FLYER
        # ==========================================

        self.fly_direction = 1

        self.fly_speed = 1.5

        self.fly_top = y - 40

        self.fly_bottom = y + 40

    # ==============================================
    # UPDATE
    # ==============================================

    def update(self):

        if not self.alive:
            return

        if self.enemy_type == "slime":

            self.move_horizontal()

        elif self.enemy_type == "fast":

            self.move_horizontal()

        elif self.enemy_type == "jumper":

            self.move_horizontal()

            self.update_jump()

        elif self.enemy_type == "flyer":

            self.move_horizontal()

            self.update_fly()

        elif self.enemy_type == "heavy":

            self.move_horizontal()

    # ==============================================
    # HORIZONTAL MOVEMENT
    # ==============================================

    def move_horizontal(self):

        self.rect.x += (
            self.speed
            * self.direction
        )

        if self.rect.left <= self.left_limit:

            self.rect.left = self.left_limit

            self.direction = 1

        if self.rect.right >= self.right_limit:

            self.rect.right = self.right_limit

            self.direction = -1

    # ==============================================
    # JUMPER
    # ==============================================

    def update_jump(self):

        self.jump_timer += 1

        if (
            self.jump_timer >= self.jump_delay
            and self.velocity_y == 0
        ):

            self.velocity_y = (
                self.jump_strength
            )

            self.jump_timer = 0

        self.velocity_y += self.gravity

        self.rect.y += int(
            self.velocity_y
        )

        if self.platform_top is not None:

            if (
                self.rect.bottom >= self.platform_top
                and self.velocity_y > 0
            ):

                self.rect.bottom = (
                    self.platform_top
                )

                self.velocity_y = 0

    # ==============================================
    # FLYER
    # ==============================================

    def update_fly(self):

        self.rect.y += (
            self.fly_speed
            * self.fly_direction
        )

        if self.rect.top <= self.fly_top:

            self.rect.top = self.fly_top

            self.fly_direction = 1

        if self.rect.bottom >= self.fly_bottom:

            self.rect.bottom = self.fly_bottom

            self.fly_direction = -1

    # ==============================================
    # PLAYER COLLISION
    # ==============================================

    def check_collision(self, player):

        if not self.alive:
            return False

        return self.rect.colliderect(
            player.rect
        )

    # ==============================================
    # DRAW
    # ==============================================

    def draw(self, screen, camera):

        if not self.alive:
            return

        camera_rect = camera.apply(
            self.rect
        )

        # ==========================================
        # BODY COLOR
        # ==========================================

        if self.enemy_type == "fast":

            body_color = (
                220,
                70,
                70
            )

        elif self.enemy_type == "jumper":

            body_color = (
                220,
                190,
                50
            )

        elif self.enemy_type == "flyer":

            body_color = (
                60,
                150,
                210
            )

        elif self.enemy_type == "heavy":

            body_color = (
                80,
                80,
                90
            )

        else:

            body_color = (
                120,
                70,
                190
            )

        # ==========================================
        # HEAVY BODY
        # ==========================================

        if self.enemy_type == "heavy":

            pygame.draw.rect(
                screen,
                body_color,
                camera_rect,
                border_radius=8
            )

        else:

            pygame.draw.ellipse(
                screen,
                body_color,
                camera_rect
            )

        # ==========================================
        # FLYER WINGS
        # ==========================================

        if self.enemy_type == "flyer":

            left_wing = pygame.Rect(
                camera_rect.x - 10,
                camera_rect.y + 10,
                15,
                20
            )

            right_wing = pygame.Rect(
                camera_rect.right - 5,
                camera_rect.y + 10,
                15,
                20
            )

            pygame.draw.ellipse(
                screen,
                body_color,
                left_wing
            )

            pygame.draw.ellipse(
                screen,
                body_color,
                right_wing
            )

        # ==========================================
        # EYES
        # ==========================================

        eye_y = (
            camera_rect.y
            + camera_rect.height // 3
        )

        left_eye = (
            camera_rect.x
            + camera_rect.width // 3,
            eye_y
        )

        right_eye = (
            camera_rect.x
            + (camera_rect.width * 2) // 3,
            eye_y
        )

        eye_size = 6

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            left_eye,
            eye_size
        )

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            right_eye,
            eye_size
        )

        pygame.draw.circle(
            screen,
            (0, 0, 0),
            left_eye,
            3
        )

        pygame.draw.circle(
            screen,
            (0, 0, 0),
            right_eye,
            3
        )