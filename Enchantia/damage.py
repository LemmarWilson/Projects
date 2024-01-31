import pygame


class Damage(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, damage, color):
        pygame.sprite.Sprite.__init__(self)

        # Define font
        font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 20)

        # Render the damage text
        self.image = font.render(str(damage), True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos, y_pos)
        self.counter = 0  # Counter to keep track of time

    def update(self, screen_scroll):
        # Repostion the damage text based on the screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        # Move the damage text upward
        self.rect.y -= 1

        # Remove the text after a few frames (approx. 1 second at 30 FPS)
        self.counter += 1
        if self.counter > 30:
            self.kill()  # Remove the sprite from the group
