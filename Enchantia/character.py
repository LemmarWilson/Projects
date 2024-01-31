import pygame
import math

import weapon
import constants


class Character:
    def __init__(self, x, y, health, animation_lists, boss, size, char_type=0):
        """
        Initialize a character.
        Args:
            x (int): Initial x-coordinate.
            Y (int): Initial y-coordinate.
            Animation_lists (List[List[pygame.Surface]]): Lists of animation frames for different actions.
        """
        self.score = 0
        self.boss = boss
        self.running = False
        self.health = health
        self.animation_lists = animation_lists
        self.action = 0  # Default to idle, 0: Idle, 1: Run
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.alive = True
        self.char_type = char_type
        self.hit = False
        self.last_hit = pygame.time.get_ticks()
        self.last_attack = pygame.time.get_ticks()
        self.stunned = False

        # Image variables
        self.image = self.animation_lists[self.action][self.frame_index]
        self.flip = False
        self.rect = pygame.Rect(
            0, 0, constants.TILE_SIZE * size, constants.TILE_SIZE * size
        )
        self.rect.center = (x, y)

    def move(self, dx, dy, obstacles_tiles, exit_tile=None):
        """
        Move the character.
        Args:
            dx (float): Change in x-coordinate.
            Dy (float): Change in y-coordinate.
            :param exit_tile:
            :param obstacles_tiles:
            :param dx:
            :param dy:
        """

        # Define movement variables
        screen_scroll = [0, 0]
        level_complete = False

        # Reset movement variables
        self.running = False
        if dx != 0 or dy != 0:
            self.running = True

        # Flip image based on a direction
        if dx < 0:
            self.flip = True
        if dx > 0:
            self.flip = False

        # Control diagonal speed
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2) / 2)
            dy = dy * (math.sqrt(2) / 2)

        # Check for collision with a map in x direction
        self.rect.x += dx
        for tile in obstacles_tiles:
            # Check for collision with a tile
            if tile[1].colliderect(self.rect):
                # Check if the collision is from right or left
                if dx > 0:
                    self.rect.right = tile[1].left
                if dx < 0:
                    self.rect.left = tile[1].right

        # Check for collision with a map in y direction
        self.rect.y += dy
        for tile in obstacles_tiles:
            # Check for collision with a tile
            if tile[1].colliderect(self.rect):
                # Check if the collision is from up or down
                if dy > 0:
                    self.rect.bottom = tile[1].top
                if dy < 0:
                    self.rect.top = tile[1].bottom

        """
                                    +++++++++++++++++++++++++++++
                                        Logic for player only
                                    +++++++++++++++++++++++++++++
        """

        # Check if outside the screen, player only
        if self.char_type == 0:
            # Check collision with an exit ladder
            if exit_tile[1].colliderect(self.rect):
                # Ensure player is close to the center of the exit ladder
                exit_dist = math.sqrt(
                    ((self.rect.centerx - exit_tile[1].centerx) ** 2)
                    + ((self.rect.centery - exit_tile[1].centery) ** 2)
                )
                if exit_dist < 20:
                    print("Level complete!")
                    level_complete = True

            # Update scroll based on player position
            # Move camera left or right
            if self.rect.right > constants.SCREEN_WIDTH - constants.SCROLL_THRESHOLD:
                screen_scroll[0] = (
                    constants.SCREEN_WIDTH - constants.SCROLL_THRESHOLD
                ) - self.rect.right
                # Update rect position
                self.rect.right = constants.SCREEN_WIDTH - constants.SCROLL_THRESHOLD
            if self.rect.left < constants.SCROLL_THRESHOLD:
                screen_scroll[0] = constants.SCROLL_THRESHOLD - self.rect.left
                # Update rect position
                self.rect.left = constants.SCROLL_THRESHOLD

            # Move the camera up or down
            if self.rect.bottom > constants.SCREEN_HEIGHT - constants.SCROLL_THRESHOLD:
                screen_scroll[1] = (
                    constants.SCREEN_HEIGHT - constants.SCROLL_THRESHOLD
                ) - self.rect.bottom
                # Update rect position
                self.rect.bottom = constants.SCREEN_HEIGHT - constants.SCROLL_THRESHOLD
            if self.rect.top < constants.SCROLL_THRESHOLD:
                screen_scroll[1] = constants.SCROLL_THRESHOLD - self.rect.top
                # Update rect position
                self.rect.top = constants.SCROLL_THRESHOLD

        # Return the screen scroll
        return screen_scroll, level_complete

    def ai(self, player, obstacles_tiles, screen_scroll, fireball_image):
        # Initialize AI variables
        fireball = None
        clipped_line = ()
        stun_cooldown = 100
        ai_dx = 0
        ai_dy = 0

        # Reposition the character based on the screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        # Create a line of sight from the enemy to the player
        line_of_sight = (
            (self.rect.centerx, self.rect.centery),
            (player.rect.centerx, player.rect.centery),
        )

        # Check if the line of sight collides with the obstacle tiles
        for tile in obstacles_tiles:
            if tile[1].clipline(line_of_sight):
                clipped_line = tile[1].clipline(line_of_sight)

        # Check if the player is close
        dist = math.sqrt(
            ((self.rect.centerx - player.rect.centerx) ** 2)
            + ((self.rect.centery - player.rect.centery) ** 2)
        )

        # If the player is close
        if not clipped_line and dist > constants.ENEMY_RANGE:
            # Make the enemy move towards the player
            if self.rect.centerx > player.rect.centerx:
                ai_dx = -constants.ENEMY_SPEED
            if self.rect.centerx < player.rect.centerx:
                ai_dx = constants.ENEMY_SPEED
            if self.rect.centery > player.rect.centery:
                ai_dy = -constants.ENEMY_SPEED
            if self.rect.centery < player.rect.centery:
                ai_dy = constants.ENEMY_SPEED

        if self.alive:
            if not self.stunned:
                # Move towards the player
                self.move(ai_dx, ai_dy, obstacles_tiles)

                # Attack player
                if dist < constants.ATTACK_RANGE and player.hit is False:
                    player.health -= 10
                    player.hit = True
                    player.last_hit = pygame.time.get_ticks()

                # Boss enemy shoots fireball
                fireball_cooldown = 700
                if self.boss:
                    if dist < 500:
                        if (
                            pygame.time.get_ticks() - self.last_attack
                            >= fireball_cooldown
                        ):
                            fireball = weapon.Fireball(
                                fireball_image,
                                self.rect.centerx,
                                self.rect.centery,
                                player.rect.centerx,
                                player.rect.centery,
                            )
                            self.last_attack = pygame.time.get_ticks()
            # Check if hit
            if self.hit:
                self.hit = False
                self.last_hit = pygame.time.get_ticks()
                self.stunned = True
                self.running = False
                self.update_action(0)  # 0: Idle

            if (pygame.time.get_ticks() - self.last_hit) > stun_cooldown:
                self.stunned = False
        return fireball

    def update(self):
        """
        Update the character's state.
        """
        # Check if the character is alive
        if self.health <= 0:
            self.health = 0
            self.alive = False

        # Timer to reset player taking hit
        hit_cooldown = 1000
        if self.char_type == 0:
            if self.hit and (pygame.time.get_ticks() - self.last_hit) > hit_cooldown:
                self.hit = False

        # Check what action the player is performing
        if self.running:
            self.update_action(1)  # 1: Run
        else:
            self.update_action(0)  # 0: Idle

        animation_cooldown = 70

        # Handle animation
        self.animate()

        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

            if self.frame_index >= len(self.animation_lists[self.action]):
                self.frame_index = 0

    def update_action(self, new_action):
        """
        Update the character's action.
        Args:
            new_action (int): New action code.
        """
        # Check if the new action is different from the previous one
        if new_action != self.action:
            self.action = new_action
            # Reset the animation
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def animate(self):
        """Animate the character."""
        # Update image depending on the current frame and animation type
        self.image = self.animation_lists[self.action][self.frame_index]

    def draw(self, surface):
        """
        Draw the character on the surface.
        Args:
            surface (pygame.Surface): The surface to draw on.
        """
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        if (
            self.char_type == 0
        ):  # Only apply offset for elf character because the image has the empty space above
            surface.blit(
                flipped_image,
                (self.rect.x, self.rect.y - constants.SCALE * constants.OFFSET),
            )
        else:
            surface.blit(flipped_image, self.rect)