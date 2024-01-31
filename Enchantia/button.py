import pygame


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, surface):
        action = False

        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Check for mouse over and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                print("Click!")
                action = True

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
