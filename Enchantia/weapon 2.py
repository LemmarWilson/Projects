import pygame
import math
import random

import constants


class Weapon:
    def __init__(self, image, arrow_image):
        """
        Initialize a weapon.

        Args:
            image (pygame.Surface): The weapon image.
        """
        self.original_image = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.arrow_image = arrow_image
        self.rect = self.image.get_rect()
        self.fired = False
        self.last_fired = pygame.time.get_ticks()

    def update(self, player):
        """
        Update the weapon's state.

        Args:
            player (Character): The player character.
        """
        shot_cooldown = 300
        arrow = None

        self.rect.center = player.rect.center

        # Get mouse position
        pos = pygame.mouse.get_pos()
        x_distance = pos[0] - self.rect.centerx
        y_distance = -(
            pos[1] - self.rect.centery
        )  # -ve because y-axis increases going down

        # Calculate angle
        self.angle = math.degrees(math.atan2(y_distance, x_distance))

        # Shooting the weapon
        if (
            pygame.mouse.get_pressed()[0]
            and self.fired is False
            and (pygame.time.get_ticks() - self.last_fired) >= shot_cooldown
        ):
            # Create arrow
            arrow = Arrow(
                self.arrow_image, self.rect.centerx, self.rect.centery, self.angle
            )
            self.fired = True
            self.last_fired = pygame.time.get_ticks()
        # Reset mouse click
        elif not pygame.mouse.get_pressed()[0]:
            self.fired = False

        return arrow

    def draw(self, surface):
        """
        Draw the weapon on the surface.

        Args:
            surface (pygame.Surface): The surface to draw on.
        """
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(
            self.image,
            (
                (self.rect.centerx - int(self.image.get_width() / 2)),
                (self.rect.centery - int(self.image.get_height() / 2)),
            ),
        )


class Arrow(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        """
        Initialize an arrow sprite.

        Args:
            image (pygame.Surface): The arrow image.
            X (int): X-coordinate of the arrow.
            Y (int): Y-coordinate of the arrow.
            Angle (float): Angle of the arrow in degrees.
        """
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Calculate velocity based on an angle
        self.dx = math.cos(math.radians(self.angle)) * constants.ARROW_SPEED
        self.dy = -(
            math.sin(math.radians(self.angle)) * constants.ARROW_SPEED
        )  # -ve because y-axis increases going down

    def update(self, screen_scroll, obstacles_tiles, enemy_list):
        """
        Update the arrow's position and check for collisions with enemies.

        Args:
            enemy_list (List[Character]): List of enemy characters.
            :param enemy_list:
            :param screen_scroll:
        """
        # Reset the damage
        damage = 0
        damage_pos = None

        # Reposition the arrow based on its velocity and screen scroll
        self.rect.x += screen_scroll[0] + self.dx
        self.rect.y += screen_scroll[1] + self.dy

        # Check for collisions between arrow and tiles walls
        for obstacle in obstacles_tiles:
            if obstacle[1].colliderect(self.rect):
                self.kill()

        # Check if the arrow is off the screen
        if (
            self.rect.left > constants.SCREEN_WIDTH
            or self.rect.right < 0
            or self.rect.top > constants.SCREEN_HEIGHT
            or self.rect.bottom < 0
        ):
            self.kill()

        # Check collisions between the arrow and the enemies
        for enemy in enemy_list:
            if enemy.rect.colliderect(self.rect) and enemy.alive:
                # Calculate the damage randomly
                damage = 10 + random.randint(-5, 5)
                damage_pos = enemy.rect
                enemy.health -= damage
                enemy.hit = True
                self.kill()
                break
        return damage, damage_pos

    def draw(self, surface):
        """
        Draw the arrow on the given surface.

        Args:
            surface (pygame.Surface): The surface to draw the arrow on.
        """
        surface.blit(
            self.image,
            (
                (self.rect.centerx - int(self.image.get_width() / 2)),
                (self.rect.centery - int(self.image.get_height() / 2)),
            ),
        )


class Fireball(pygame.sprite.Sprite):
    def __init__(self, image, x, y, target_x, target_y):
        """
        Initialize an arrow sprite.

        Args:
            image (pygame.Surface): The arrow image.
            X (int): X-coordinate of the arrow.
            Y (int): Y-coordinate of the arrow.
            Angle (float): Angle of the arrow in degrees.
        """
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        x_dist = target_x - x
        y_dist = -(target_y - y)
        self.angle = math.degrees(math.atan2(y_dist, x_dist))
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Calculate velocity based on an angle
        self.dx = math.cos(math.radians(self.angle)) * constants.FIREBALL_SPEED
        self.dy = -(
            math.sin(math.radians(self.angle)) * constants.FIREBALL_SPEED
        )  # -ve because y-axis increases going down

    def update(self, screen_scroll, player):
        """
        Update the arrow's position and check for collisions with enemies.

        Args:
            enemy_list (List[Character]): List of enemy characters.
            :param player:
            :param screen_scroll:
        """

        # Reposition the arrow based on its velocity and screen scroll
        self.rect.x += screen_scroll[0] + self.dx
        self.rect.y += screen_scroll[1] + self.dy

        # Check if the fireball is off the screen
        if (
            self.rect.left > constants.SCREEN_WIDTH
            or self.rect.right < 0
            or self.rect.top > constants.SCREEN_HEIGHT
            or self.rect.bottom < 0
        ):
            self.kill()

        # Check for collisions between the fireball and the player
        if player.rect.colliderect(self.rect) and player.hit == False:
            player.hit = True
            player.last_hit = pygame.time.get_ticks()
            player.health -= 10
            self.kill()

    def draw(self, surface):
        """
        Draw the arrow on the given surface.

        Args:
            surface (pygame.Surface): The surface to draw the arrow on.
        """
        surface.blit(
            self.image,
            (
                (self.rect.centerx - int(self.image.get_width() / 2)),
                (self.rect.centery - int(self.image.get_height() / 2)),
            ),
        )
