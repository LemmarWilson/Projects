import pygame

import constants


class ScreenFade:
    def __init__(self, screen, direction, colour, speed):
        self.screen = screen
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False

        self.fade_counter += self.speed
        if self.direction == 1:  # the whole screen fades every direction outwards
            # Left Fade
            pygame.draw.rect(
                self.screen,
                self.colour,
                (
                    0 - self.fade_counter,
                    0,
                    constants.SCREEN_WIDTH // 2,
                    constants.SCREEN_HEIGHT,
                ),
            )
            # Right Fade
            pygame.draw.rect(
                self.screen,
                self.colour,
                (
                    constants.SCREEN_WIDTH // 2 + self.fade_counter,
                    0,
                    constants.SCREEN_WIDTH,
                    constants.SCREEN_HEIGHT,
                ),
            )
            # Top Fade
            pygame.draw.rect(
                self.screen,
                self.colour,
                (
                    0,
                    0 - self.fade_counter,
                    constants.SCREEN_WIDTH,
                    constants.SCREEN_HEIGHT // 2,
                ),
            )
            # Bottom Fade
            pygame.draw.rect(
                self.screen,
                self.colour,
                (
                    0,
                    constants.SCREEN_HEIGHT // 2 + self.fade_counter,
                    constants.SCREEN_WIDTH,
                    constants.SCREEN_HEIGHT,
                ),
            )
        elif self.direction == 2:  # the whole screen fades every direction inwards
            # Top going down
            pygame.draw.rect(
                self.screen,
                self.colour,
                (0, 0, constants.SCREEN_WIDTH, 0 + self.fade_counter),
            )

            # Bottom going up
            pygame.draw.rect(
                self.screen,
                self.colour,
                (
                    0,
                    constants.SCREEN_HEIGHT - self.fade_counter,
                    constants.SCREEN_WIDTH,
                    constants.SCREEN_HEIGHT,
                ),
            )

            # Left going right
            pygame.draw.rect(
                self.screen,
                self.colour,
                (
                    0,
                    0,
                    0 + self.fade_counter,
                    constants.SCREEN_HEIGHT,
                ),
            )

            # Right going left
            pygame.draw.rect(
                self.screen,
                self.colour,
                (
                    constants.SCREEN_WIDTH - self.fade_counter,
                    0,
                    constants.SCREEN_WIDTH,
                    constants.SCREEN_HEIGHT,
                ),
            )

        if self.fade_counter >= constants.SCREEN_WIDTH:
            fade_complete = True
        return fade_complete
